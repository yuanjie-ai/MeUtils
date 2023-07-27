#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : Neo4j
# @Time         : 2020/9/18 11:26 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://zhuanlan.zhihu.com/p/437824721
# https://blog.csdn.net/juanjuan1314/article/details/90814788

from meutils.pipe import *
from py2neo import Graph, Node, Relationship
from concurrent.futures import ThreadPoolExecutor


class Neo4j(object):
    """TODO
    添加属性值：关系的属性
    """

    def __init__(self, profile="bolt://xx:7687", name='neo4j', password='ai', **settings):
        self.graph = Graph(profile, auth=(name, password), **settings).run
        # self.graph.delete_all()
        self.node_labels = self.graph.schema.node_labels  # 查看图结构中节点标签的类别，返回结果是一个frozenset
        self.relationship_types = self.graph.schema.relationship_types  # 查看图结构中关系的类型
        # graph.schema.get_indexes

    def create_nodes(self, df_nodes, label="Demo", max_workers=30):
        """

        :param label: Node Label 可以理解为一个集合
        :param node_list: [(k, v, r), ] 三元组
        :return:
        """
        df_nodes.columns = ['k', 'v', 'r']
        groups = df_nodes.groupby('k')
        print(f"Num Group: {len(groups)}")

        func = lambda group: [self._create_node(label, nodes) for nodes in tqdm(group[1].values)]

        with ThreadPoolExecutor(max_workers, thread_name_prefix=f"{label}__") as pool:
            _ = pool.map(func, tqdm(groups), chunksize=1)

    def _create_node(self, label, nodes):
        k, v, r = nodes

        node_key = self._create(label, k)
        node_value = self._create(label, v)

        if node_key != node_value:
            node_relation = Relationship(node_key, r, node_value)  # r也可以是节点，
            # node_relation['属性'] = 0
            self.graph.create(node_relation)

    @lru_cache(1024)
    def _create(self, label, name):
        subgraph = Node(label, name=name)  # properties 属性信息
        self.graph.create(subgraph)
        return subgraph


