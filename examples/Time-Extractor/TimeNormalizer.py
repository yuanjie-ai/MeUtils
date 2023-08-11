#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : TimeNormalizer.py
# @Software: PyCharm
import pickle
import regex as re
import arrow
import json
import os
import sys
import pandas as pd

from StringPreHandler import StringPreHandler
from TimePoint import TimePoint
from TimeUnit import TimeUnit


# 时间表达式识别的主要工作类
class TimeNormalizer:
    def __init__(self, isPreferFuture=False):
        self.isPreferFuture = isPreferFuture
        self.pattern, self.holi_solar, self.holi_lunar = self.init()

    # 这里对一些不规范的表达做转换
    def _filter(self, input_query):
        # 这里对于下个周末这种做转化 把个给移除掉
        input_query = StringPreHandler.numberTranslator(input_query)

        rule = u"[0-9]月[0-9]"
        pattern = re.compile(rule)
        match = pattern.search(input_query)
        if match != None:
            index = input_query.find('月')
            rule = u"日|号"
            pattern = re.compile(rule)
            match = pattern.search(input_query[index:])
            if match == None:
                rule = u"[0-9]月[0-9]+"
                pattern = re.compile(rule)
                match = pattern.search(input_query)
                if match != None:
                    end = match.span()[1]
                    input_query = input_query[:end] + '号' + input_query[end:]

        rule = u"月"
        pattern = re.compile(rule)
        match = pattern.search(input_query)
        if match == None:
            input_query = input_query.replace('个', '')

        input_query = input_query.replace('中旬', '15号')
        # input_query = input_query.replace('傍晚', '午后')
        input_query = input_query.replace('大年', '')
        input_query = input_query.replace('五一', '劳动节')
        input_query = input_query.replace('白天', '早上')
        input_query = input_query.replace('：', ':')
        return input_query

    def init(self):
        fpath = os.path.dirname(__file__) + '/resource/reg.pkl'
        try:
            with open(fpath, 'rb') as f:
                pattern = pickle.load(f)
        except:
            with open(os.path.dirname(__file__) + '/resource/regex.txt', 'r', encoding = "utf-8") as f:
                content = f.read()
            p = re.compile(content)
            with open(fpath, 'wb') as f:
                pickle.dump(p, f)
            with open(fpath, 'rb') as f:
                pattern = pickle.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_solar.json', 'r', encoding = 'utf-8') as f:
            holi_solar = json.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_lunar.json', 'r', encoding = 'utf-8') as f:
            holi_lunar = json.load(f)
        return pattern, holi_solar, holi_lunar

    def parse(self, target, timeBase=arrow.now()):
        """
        TimeNormalizer的构造方法，timeBase取默认的系统当前时间
        :param timeBase: 基准时间点
        :param target: 待分析字符串
        :return: 时间单元数组
        """
        self.isTimeSpan = False
        self.invalidSpan = False
        self.timeSpan = ''
        self.target = self._filter(target)
        self.timeBase = arrow.get(timeBase).format('YYYY-M-D-H-m-s')
        self.nowTime = timeBase
        self.oldTimeBase = self.timeBase
        self.__preHandling()
        dic = {}
        dic = self._filter_regular(dic)
        if dic:
            return json.dumps(dic)

        self.timeToken = self.__timeEx()
        res = self.timeToken

        if self.isTimeSpan:
            if self.invalidSpan:
                dic['error'] = 'no time pattern could be extracted.'
            else:
                result = {}
                dic['type'] = 'timedelta'
                dic['timedelta'] = self.timeSpan
                # print(dic['timedelta'])
                index = dic['timedelta'].find('days')

                days = int(dic['timedelta'][:index - 1])
                result['year'] = int(days / 365)
                result['month'] = int(days / 30 - result['year'] * 12)
                result['day'] = int(days - result['year'] * 365 - result['month'] * 30)
                index = dic['timedelta'].find(',')
                time = dic['timedelta'][index + 1:]
                time = time.split(':')
                result['hour'] = int(time[0])
                result['minute'] = int(time[1])
                result['second'] = int(time[2])
                dic['timedelta'] = result
        else:
            if len(res) == 0:
                dic['error'] = 'no time pattern could be extracted.'
            elif len(res) == 1:
                dic['type'] = 'timestamp'
                dic['timestamp'] = res[0].time.format("YYYY-MM-DD HH:mm:ss")
            else:
                dic['type'] = 'timespan'
                if res[1].time < res[0].time:
                    res[1].time = res[1].time.shift(days=1)
                dic['timespan'] = [res[0].time.format("YYYY-MM-DD HH:mm:ss"), res[1].time.format("YYYY-MM-DD HH:mm:ss")]
        return json.dumps(dic)

    def __preHandling(self):
        """
        待匹配字符串的清理空白符和语气助词以及大写数字转化的预处理
        :return:
        """
        self.target = StringPreHandler.delKeyword(self.target, u"\\s+")  # 清理空白符
        self.target = StringPreHandler.delKeyword(self.target, u"[的]+")  # 清理语气助词
        self.target = StringPreHandler.numberTranslator(self.target)  # 大写数字转化

    def __timeEx(self):
        """

        :param target: 输入文本字符串
        :param timeBase: 输入基准时间
        :return: TimeUnit[]时间表达式类型数组
        """
        startline = -1
        endline = -1
        rpointer = 0
        time_extractor = []

        match = self.pattern.finditer(self.target)
        for m in match:
            startline = m.start()
            if startline == endline:
                rpointer -= 1
                time_extractor[rpointer] = time_extractor[rpointer] + m.group()
            else:
                time_extractor.append(m.group())
            endline = m.end()
            rpointer += 1

        res = []
        # 时间上下文： 前一个识别出来的时间会是下一个时间的上下文，用于处理：周六3点到5点这样的多个时间的识别，第二个5点应识别到是周六的。
        contextTp = TimePoint()
        # print(self.timeBase)
        print('time_extractor:', time_extractor)
        for i in range(0, rpointer):
            # 这里是一个类嵌套了一个类
            res.append(TimeUnit(time_extractor[i], self, contextTp))
            # res[i].tp.tunit[3] = -1
            contextTp = res[i].tp
            # print(self.nowTime.year)
            # print(contextTp.tunit)
        res = self.__filterTimeUnit(res)

        return res

    def __filterTimeUnit(self, tu_arr):
        """
        过滤timeUnit中无用的识别词。无用识别词识别出的时间是1970.01.01 00:00:00(fastTime=0)
        :param tu_arr:
        :return:
        """
        if (tu_arr is None) or (len(tu_arr) < 1):
            return tu_arr
        res = []
        for tu in tu_arr:
            if tu.time.timestamp != 0:
                res.append(tu)
        return res

    def _filter_regular(self,dic):
        # 规则数字日期格式匹配
        if len(self.target)==10:
            # yyyy-mm-dd
            p1 = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})'
                            r'-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)'
                            r'-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|('
                            r'(([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00)'
                            r')-02-29)')
            # yyyy.mm.dd
            p2 = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})'
                     r'.(((0[13578]|1[02]).(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)'
                     r'.(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|('
                     r'(([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00)'
                     r').02.29)')
            # # yyyy/mm/dd
            p3 = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})'
                     r'/(((0[13578]|1[02])/(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)'
                     r'/(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|('
                     r'(([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00)'
                     r')/02/29)')
            m1 = p1.search(self.target)
            m2 = p2.search(self.target)
            m3 = p3.search(self.target)
            if m1:
                print('time_extractor:', m1.group())
                dic['type'] = 'timestamp'
                dic['timestamp'] = pd.to_datetime(m1.group()).strftime('%Y-%m-%d %H:%M:%S')
            elif m2:
                print('time_extractor:', m2.group())
                dic['type'] = 'timestamp'
                dic['timestamp'] = pd.to_datetime(m2.group()).strftime('%Y-%m-%d %H:%M:%S')
            elif m3:
                print('time_extractor:', m3.group())
                dic['type'] = 'timestamp'
                dic['timestamp'] = pd.to_datetime(m3.group()).strftime('%Y-%m-%d %H:%M:%S')
        elif len(self.target)==8:
            # yyyymmdd
            p4 = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9]'
                            r'[0-9]{3})(((0[13578]|1[02])(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)'
                            r'(0[1-9]|[12][0-9]|30))|(02(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})'
                            r'(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))'
                            r'0229)')
            m4 = p4.search(self.target)
            if m4:
                print('time_extractor:', m4.group())
                dic['type'] = 'timestamp'
                dic['timestamp'] = pd.to_datetime(m4.group()).strftime('%Y-%m-%d %H:%M:%S')
        return dic