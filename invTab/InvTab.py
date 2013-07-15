#!/usr/bin/env python
#coding=gbk

'''
实现倒排索引，并用bm25 rank
'''

import sys
import math

k1 = 2
b = 0.75

class Doc():
    def __init__(self):
        self.content = ''
        self.wordCnt = 0

class InvTab():
    def __init__(self):
        self.docLst = []  ## 存储未分词doc
        self.invDic = {}  ## 存储排序好的倒排表
        self.idfDic = {}  ## 存储idf数值
        self.aveDocLen = 0  ## 存储文档平均长度

    def insert(self, doc):
        doc = doc.strip()
        if not doc:
            return
        docID = len(self.docLst)  ## docID从小到大，保证倒排表是有序的
        
        wordDic = {}  ## 统计单词频度
        wordCnt = 0  ## 统计doc长度
        for w in doc.split():  ## 默认传入时已分好词
            wordCnt += 1
            if w in wordDic:
                wordDic[w] += 1
            else:
                wordDic[w] =  1
        
        docNode = Doc()  ## 新建一个doc入库
        docNode.content = doc
        docNode.wordCnt = wordCnt
        self.docLst.append(docNode)
        self.aveDocLen += wordCnt
        
        for w in wordDic:
            if w in self.invDic:
                self.invDic[w].append((docID, wordDic[w] * 1.0 / wordCnt))  ## 倒排表中存储docID和DF
            else:
                self.invDic[w] = [(docID, wordDic[w] * 1.0 / wordCnt)]
            if w in self.idfDic:  ## 准备建立idf字典
                self.idfDic[w] += 1
            else:
                self.idfDic[w] = 1

    def fix(self):
        '''
        全部doc输入完成，已有doc数，统计idf值和文档平均长度，如果只是求交不算bm25，这步可以不做
        '''
        docCnt = len(self.docLst)
        for w in self.idfDic:
            self.idfDic[w] = math.log((docCnt - self.idfDic[w] + 0.5) / (self.idfDic[w] + 0.5))
        self.aveDocLen =  self.aveDocLen * 1.0 / docCnt
        #print >> sys.stderr, 'fix finish %s' % len(self.docLst)

    def intersectDocID(self, query):
        '''
        传入一个query，求交计算docID
        '''
        result = {}
        candiWordLst = []  ## 索引过的单词
        candiInvTab = []  ## 索引过的倒排表
        for w in query.split():
            if w in self.invDic:
                candiWordLst.append(w)
                candiInvTab.append(self.invDic[w])
        if len(candiWordLst) * 1.0 / len(query.split()) < 0.5:  ## 如果query中有一半及以上的词都没有相应倒排表，认为求交结果为空
            return {}

        index = [0] * len(candiInvTab)  ## index标记每个倒排表不断往后推移
        while True:
            maxID = candiInvTab[0][index[0]][0]  ## 第一个倒排表位于index[0]位置的docID，初始化为maxID
            isGetMax = True  ## 假定各倒排表中位于index位置的docID均相等，即求交有结果
            for i, invTab in enumerate(candiInvTab):
                if maxID != invTab[index[i]][0]:  ## 第i个倒排表中无maxID，有比maxID更大的doc，求交结果也只可能比maxID更大，置maxID为更大的值
                    isGetMax = False
                    if maxID < invTab[index[i]][0]:
                        maxID = invTab[index[i]][0]
            isEnd = False  ## 一旦有某个倒排表遍历完成，求交结束
            if isGetMax:  ## 求交有结果，每个倒排表中index往后移一位
                for i, invTab in enumerate(candiInvTab):  ## docID和DF值加入
                    if i == 0:
                        result[maxID] = {candiWordLst[i]: invTab[index[i]][1]}
                    else:
                        result[maxID][candiWordLst[i]] = invTab[index[i]][1]
                for i, invTab in enumerate(candiInvTab):  ## index往后移
                    index[i] += 1
                    if index[i] == len(invTab):  ## 第i个倒排表遍历完成
                        isEnd = True
                        break
            else:  ## 小于maxID的那些倒排表中index往后推，直到碰到大于等于maxID或遍历完成
                for i, invTab in enumerate(candiInvTab):
                    while index[i] != len(invTab) and invTab[index[i]][0] < maxID:
                        index[i] += 1
                    if index[i] == len(invTab):
                        isEnd = True
                        break
            if isEnd:
                break
        return result

    def search(self, query):
        '''
        传入一个query，求交计算docID，按bm25相关性排序
        '''
        result = []
        docIdDic = self.intersectDocID(query)
        #print >> sys.stderr, 'intersect cnt: %s' % len(docIdDic)
        wordLst = query.split()
        for docID in docIdDic:
            bm25 = 0.0
            for w in wordLst:
                if not w in self.idfDic:
                    continue
                idf = self.idfDic[w]
                df = docIdDic[docID][w]
                bm25 += idf * df * (k1 + 1) / (df + k1 * (1 - b + b * self.docLst[docID].wordCnt / self.aveDocLen))
            result.append((docID, bm25, self.docLst[docID].content))
        return sorted(result, key = lambda result: result[1], reverse = True)

def main():
    invTab = InvTab()
    fin = open(sys.argv[1])
    for line in fin:
        line = line.strip()
        if line:
            invTab.insert(line)
    fin.close()
    invTab.fix()
    while True:
        line = raw_input('>>')
        if line == 'jjjexit':
            break
        for docID, bm25, doc in invTab.search(line)[:10]:
            print '%s\t%s\t%s' % (docID, bm25, doc)

if __name__ == "__main__":
    main()
