#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : send_email
# @Time         : 2020-03-04 13:58
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :

"""
# 小米邮件
# 机器自带邮件
# 邮件代理
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ME
from meutils.pipe import *
from meutils.date_utils import date_difference
from meutils.pd_utils import df2bhtml


def send_email(subject="",
               msg: Union[str, pd.DataFrame] = "",
               receivers: Union[str, list] = 'meutils@qq.com',
               _subtype='html',
               msg_prefix='',
               msg_suffix='',
               msg_fn=lambda x: x,
               date=date_difference(fmt='%Y-%m-%d %H:%M:%S', days=0),
               host2sender=None,
               **kwargs):
    """

    :param subject: 主题
    :param msg:
    :param receivers:
    :param _subtype:
    :param msg_prefix:
    :param msg_suffix:
    :param msg_fn:
    :param kwargs:
    :return:
    """

    # init
    # token = get_zk_config("/push/email_token")
    # host, sender = list(token.items())[0]
    if host2sender is None:
        host2sender = {'localhost': 'BOT'}

    host, sender = list(host2sender.items())[0]
    smtp = smtplib.SMTP(host, 25)

    # 主题+内容
    subject = f"👉{subject}📅{date}"

    if isinstance(msg, pd.DataFrame):
        msg_fn = lambda df: df2bhtml(df, subject)
    msg = f"{msg_prefix}{msg_fn(msg)}{msg_suffix}"

    message = MIMEText(msg, _subtype, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender

    if isinstance(receivers, str) and receivers.__contains__("@"):
        receivers = [receivers]
    message['To'] = ",".join(receivers)

    try:
        smtp.sendmail(sender, receivers, message.as_string())
        logger.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger.warning(f"{e}: 无法发送邮件")


def nesc_email():
    import yagmail
    yagmail_server = yagmail.SMTP(
        user="xx@xx.cn",
        password="Qq-xx",
        host="mail.xx.cn"
    )

    contents = ['Hi, baby.', 'One', 'Two']
    yagmail_server.send('xx@xx.cn', '测试', contents)


if __name__ == '__main__':
    send_email("测试邮件", msg='邮件内容')
    send_email("测试邮件", msg=pd.DataFrame(np.random.random((5, 5))))
