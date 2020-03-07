#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
模拟盘Bars
"""


class Stack:
    """
    stack
    """
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def clear(self):
        del self.items[:]

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.items)

    def top(self):
        if self.size():
            return self.items[self.size()-1]
        else:
            return None


class Bar:
    """
    字典流数据的封装
    """
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data.get(key,None)

    def __str__(self):
        return '字典流里的数据：{}'.format(str(self.data))

    def __bool__(self):
        if self.data:
            return True
        else:
            return False


class Bars:
    def __init__(self, strategy):
        """
        策略数据
        :param strategy:
        """
        self.strategy = strategy
        self.__stack = Stack()
        self.__sync()

    def clear(self):
        """
        清除堆栈
        :return:
        """
        self.__stack.clear()

    def push(self, data):
        """
        添加数据
        :param data:
        :return:
        """
        self.__stack.push(Bar(data))

    def top(self):
        """
        获取堆栈栈顶数据
        :return:
        """
        return self.__stack.top()

    def size(self):
        """
        获取现有bar的长度
        :return:
        """
        return self.__stack.size()

    def __apply(self, row):
        """
        将策略相关的数据的大盘数据转化为按时间依次递增的bar流
        :param row:
        :return:
        """
        date = row.name
        # 获取分钟秒的执行数据
        handlers = ['M{}'.format(date.day), 'W{}'.format(date.weekday()), 'D']
        befores, afters = [], []
        for key in handlers:
            # 满足 月，周，日规则的
            handler = self.strategy.handlers.get(key, {})
            # 根据不同的类型注册到不同时间粒度的执行中
            for category, func in handler.items():
                # 开盘前执行
                if category == 'befor_open':
                    befores.extend(func)
                # 开盘后执行
                elif category == 'after_close':
                    afters.extend(func)

        # 写入到队列中
        item = {
            'date': row.date,
            'befor_day': row.befor_day,
            'befores': befores,
            'afters': afters
        }

        # 加入仓位控制等
        if hasattr(row, 'stop'):
            item['stop'] = row.stop
        if hasattr(row, 'weight'):
            item['weight'] = row.weight
            item['niubear'] = row.niubear
        # 处理完bar放到队列里等待处理
        self.push(item)

    def __sync(self):
        """
        整理数据为bars
        :return:
        """
        self.strategy.hq.apply(self.__apply, axis=1)
