#!/usr/bin/env python
#coding=gbk

'''
用hashmap实现AC自动机，支持输入为unicode，更好的匹配单字中文pattern
'''

import sys
import time

class Node():
    def __init__(self):
        self.word = None
        self.fail = None
        self.end = False
        self.next = {}

class AhoCorasick():
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        '''
        插入query
        '''
        word = word.strip()  ## 空串不插
        if not word:
            return
        p = self.root  ## p指定root
        for w in word:  ## 循环每个词
            if w in p.next:  ## 如果已插入过，指向孩子
                p = p.next[w]
            else:  ## 否则建立新节点，指向新节点
                q = Node()  ##新节点
                p.next[w] = q
                p = q
        p.word = word  ## 所有单词都建立了结点，在末结点处写word和end
        p.end = True

    def fix(self):
        '''
        建立fail指针
        '''
        self.root.fail = None
        queue = [self.root]  ## 宽度优先遍历，将根指针入队列
        while len(queue) != 0:
            parent = queue[0]
            queue.pop(0)  ## 父结点出队列
            for w in parent.next:  ## 遍历每个孩子
                child = parent.next[w]
                failp = parent.fail
                while failp != None:
                    if w in failp.next:  ## 找父结点的fail指针，看其是否有当前孩子，如果有指向即可
                        child.fail = failp.next[w]
                        break
                    failp = failp.fail  ## 否则不断找父结点的fail指针
                if failp == None:  ## 如果最终指过root，说明无法找到，当前孩子的fail指向root
                    child.fail = self.root
                queue.append(child)  ## 将孩子入队列，宽度优先处理

    def search(self, word):
        '''
        查找所有匹配子串
        '''
        result = []
        p = self.root  ## 从根结点开始查找
        for i, w in enumerate(word):  ## 主串中指针不断往前不回退
            while p != None and not w in p.next:  ## 如果当前结点不存在该单词，看其fail指针是否存在该单词
                p = p.fail
            if p == None:  ## 回溯过root节点了，说明没有找到，将p指向root
                p = self.root
            else:  ## 否则说明找到了，p指向为该单词的结点
                p = p.next[w]
            q = p  ## 判断该单词结点及其一连串fail结点是否是某个pattern的末尾
            while q != None:
                if q.end:  ## 如果是，返回该模式串，并可计算出该模式串在主串中的头尾位置
                    result.append(((i + 1 - len(q.word), i + 1), q.word))
                q = q.fail  ## 不断寻找fail结点，直到回溯过root
        return result

def main():
    aho = AhoCorasick()
    patternLst = [u'播放', u'牌', u'下载']
    ms = u'快播放器下载'
    for pattern in patternLst:
        aho.insert(pattern)
    aho.fix()
    for pos, word in aho.search(ms):
        print pos, word.encode('gbk')

    '''t1 = time.time()
    aho = AhoCorasick()
    for i, line in enumerate(sys.stdin):
        if i % 10000 == 0:
            print >> sys.stderr, i
        line = line.strip()
        aho.insert(line.decode('gbk', 'ignore'))
    t2 = time.time()
    print >> sys.stderr, 'insert time: %f' % (t2 - t1)
    aho.fix()
    t3 = time.time()
    print >> sys.stderr, 'build fail time: %f' % (t2 - t1)
    testLst = []
    fin = open(sys.argv[1])
    for i, line in enumerate(fin):
        line = line.strip()
        testLst.append(line.decode('gbk', 'ignore'))
        if i > 100000:
            break
    fin.close()
    t4 = time.time()
    for line in testLst:
        for pos, word in aho.search(line):
            print pos, word.encode('gbk', 'ignore')
        print '=================='
    t5 = time.time()
    print >> sys.stderr, 'search time: %f' % (t5 - t4)
    print >> sys.stderr, 'search ave time: %f' % ((t5 - t4) * 1.0 / len(testLst))
    print >> sys.stderr, 'will exit!'''

if __name__ == "__main__":
    main()
