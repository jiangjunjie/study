#!/usr/bin/env python
#coding=gbk

'''
用倒排思想实现ac类似的功能
缺点：pattern串不能过多，只支持unicode（或改写后支持全角，总之不能变长）
'''

import sys

class Index():
    def __init__(self):
        self.docLst = []
        self.index = {}
        self.cnt = 0

    def insert(self, doc):
        '''
        模式串入库
        '''
        if len(doc) == 1:
            self.index[doc] = [self.cnt]
            self.docLst.append(doc)
            self.cnt += 1
        elif len(doc) > 1:
            allTermInserted = True
            indexTerm = ''  ##当前doc要用哪个term来索引
            maxDoc = sys.maxint
            for i in xrange(len(doc) - 2, -1, -1):
                term = doc[i] + doc[i + 1];
                if not term in self.index:
                    indexTerm = term  ##新term来索引
                    allTermInserted = False
                    break
                else:
                    if len(self.index[term]) < maxDocNum:
                        maxDocNum = len(self.index[term])
                        indexTerm = term  ##所有term都曾经索引，选择doc数最少的一个term来索引
            if allTermInserted:
                self.index[indexTerm].append(self.cnt)
            else:
                self.index[indexTerm] = [self.cnt]
            self.docLst.append(doc)
            self.cnt += 1

    def search(self, word):
        '''
        搜索匹配子串
        '''
        result = []
        if len(word) == 1:
            if word in self.index:
                result = [(word, (0, 1))]
            return result

        docidResult = set([])
        posResult = []
        if word[-1] in self.index:  ## 最后一个字有索引
            docid = self.index[word[-1]][0]
            docidResult.add(docid)
            for pos in self.findall(word, word[-1]):
                posResult.append((pos, docid))

        for i in xrange(len(word) - 2, -1, -1):
            term = word[i] + word[i + 1]
            if term in self.index:  ## 有相应term索引
                for docid in self.index[term]:
                    if not docid in docidResult:  ## 该doc未检索过(一个doc只会在一个term的倒排里)
                        doc = self.docLst[docid]
                        posFind = self.findall(word, doc)
                        if len(posFind) > 0:
                            docidResult.add(docid)
                            for pos in posFind:
                                posResult.append((pos, docid))
            if word[i] in self.index:
                docid = self.index[word[i]][0]
                if not docid in docidResult:
                    docidResult.add(docid)
                    posFind = self.findall(word, word[i])
                    for pos in posFind:  ##至少有一个是当前
                        posResult.append((pos, docid))
        for pos, docid in sorted(posResult, key = lambda posResult: (posResult[0][0], posResult[0][1])):
            result.append((self.docLst[docid], pos))
        return result

    def findall(self, word, doc):
        '''
        计算doc在word中出现的所有位置
        '''
        result = []
        start = 0
        while True:
            index = word.find(doc, start)
            if index == -1:
                break
            result.append((index, len(word) - index - len(doc) + 1))
            start = index + 1
        return result

def main():
    index = Index()
    index.insert(u'a')
    index.insert(u'abc')
    index.insert(u'cd')
    for s, pos in index.search(u'abcdeabcd'):
        print s, pos

    index2 = Index()
    index2.insert(u'a')
    index2.insert(u'abc')
    index2.insert(u'cd')
    for s, pos in index2.search(u'a'):
        print s, pos

    index3 = Index()
    index3.insert(u'播放')
    index3.insert(u'牌')
    index3.insert(u'下载')
    for s, pos in index3.search(u'请播放器下载支持牌子下载'):
        print s.encode('gbk', 'ignore'), pos

if __name__ == "__main__":
    main()

        



