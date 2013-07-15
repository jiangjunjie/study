#!/usr/bin/env python
#coding=gbk

'''
ʵ�ֵ�������������bm25 rank
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
        self.docLst = []  ## �洢δ�ִ�doc
        self.invDic = {}  ## �洢����õĵ��ű�
        self.idfDic = {}  ## �洢idf��ֵ
        self.aveDocLen = 0  ## �洢�ĵ�ƽ������

    def insert(self, doc):
        doc = doc.strip()
        if not doc:
            return
        docID = len(self.docLst)  ## docID��С���󣬱�֤���ű��������
        
        wordDic = {}  ## ͳ�Ƶ���Ƶ��
        wordCnt = 0  ## ͳ��doc����
        for w in doc.split():  ## Ĭ�ϴ���ʱ�ѷֺô�
            wordCnt += 1
            if w in wordDic:
                wordDic[w] += 1
            else:
                wordDic[w] =  1
        
        docNode = Doc()  ## �½�һ��doc���
        docNode.content = doc
        docNode.wordCnt = wordCnt
        self.docLst.append(docNode)
        self.aveDocLen += wordCnt
        
        for w in wordDic:
            if w in self.invDic:
                self.invDic[w].append((docID, wordDic[w] * 1.0 / wordCnt))  ## ���ű��д洢docID��DF
            else:
                self.invDic[w] = [(docID, wordDic[w] * 1.0 / wordCnt)]
            if w in self.idfDic:  ## ׼������idf�ֵ�
                self.idfDic[w] += 1
            else:
                self.idfDic[w] = 1

    def fix(self):
        '''
        ȫ��doc������ɣ�����doc����ͳ��idfֵ���ĵ�ƽ�����ȣ����ֻ���󽻲���bm25���ⲽ���Բ���
        '''
        docCnt = len(self.docLst)
        for w in self.idfDic:
            self.idfDic[w] = math.log((docCnt - self.idfDic[w] + 0.5) / (self.idfDic[w] + 0.5))
        self.aveDocLen =  self.aveDocLen * 1.0 / docCnt
        #print >> sys.stderr, 'fix finish %s' % len(self.docLst)

    def intersectDocID(self, query):
        '''
        ����һ��query���󽻼���docID
        '''
        result = {}
        candiWordLst = []  ## �������ĵ���
        candiInvTab = []  ## �������ĵ��ű�
        for w in query.split():
            if w in self.invDic:
                candiWordLst.append(w)
                candiInvTab.append(self.invDic[w])
        if len(candiWordLst) * 1.0 / len(query.split()) < 0.5:  ## ���query����һ�뼰���ϵĴʶ�û����Ӧ���ű���Ϊ�󽻽��Ϊ��
            return {}

        index = [0] * len(candiInvTab)  ## index���ÿ�����ű�����������
        while True:
            maxID = candiInvTab[0][index[0]][0]  ## ��һ�����ű�λ��index[0]λ�õ�docID����ʼ��ΪmaxID
            isGetMax = True  ## �ٶ������ű���λ��indexλ�õ�docID����ȣ������н��
            for i, invTab in enumerate(candiInvTab):
                if maxID != invTab[index[i]][0]:  ## ��i�����ű�����maxID���б�maxID�����doc���󽻽��Ҳֻ���ܱ�maxID������maxIDΪ�����ֵ
                    isGetMax = False
                    if maxID < invTab[index[i]][0]:
                        maxID = invTab[index[i]][0]
            isEnd = False  ## һ����ĳ�����ű������ɣ��󽻽���
            if isGetMax:  ## ���н����ÿ�����ű���index������һλ
                for i, invTab in enumerate(candiInvTab):  ## docID��DFֵ����
                    if i == 0:
                        result[maxID] = {candiWordLst[i]: invTab[index[i]][1]}
                    else:
                        result[maxID][candiWordLst[i]] = invTab[index[i]][1]
                for i, invTab in enumerate(candiInvTab):  ## index������
                    index[i] += 1
                    if index[i] == len(invTab):  ## ��i�����ű�������
                        isEnd = True
                        break
            else:  ## С��maxID����Щ���ű���index�����ƣ�ֱ���������ڵ���maxID��������
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
        ����һ��query���󽻼���docID����bm25���������
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
