#!/usr/bin/env python
#coding=gbk

'''
�õ���˼��ʵ��ac���ƵĹ���
ȱ�㣺pattern�����ܹ��ֻ֧࣬��unicode�����д��֧��ȫ�ǣ���֮���ܱ䳤��
'''

import sys

class Index():
    def __init__(self):
        self.docLst = []
        self.index = {}
        self.cnt = 0

    def insert(self, doc):
        '''
        ģʽ�����
        '''
        if len(doc) == 1:
            self.index[doc] = [self.cnt]
            self.docLst.append(doc)
            self.cnt += 1
        elif len(doc) > 1:
            allTermInserted = True
            indexTerm = ''  ##��ǰdocҪ���ĸ�term������
            maxDoc = sys.maxint
            for i in xrange(len(doc) - 2, -1, -1):
                term = doc[i] + doc[i + 1];
                if not term in self.index:
                    indexTerm = term  ##��term������
                    allTermInserted = False
                    break
                else:
                    if len(self.index[term]) < maxDocNum:
                        maxDocNum = len(self.index[term])
                        indexTerm = term  ##����term������������ѡ��doc�����ٵ�һ��term������
            if allTermInserted:
                self.index[indexTerm].append(self.cnt)
            else:
                self.index[indexTerm] = [self.cnt]
            self.docLst.append(doc)
            self.cnt += 1

    def search(self, word):
        '''
        ����ƥ���Ӵ�
        '''
        result = []
        if len(word) == 1:
            if word in self.index:
                result = [(word, (0, 1))]
            return result

        docidResult = set([])
        posResult = []
        if word[-1] in self.index:  ## ���һ����������
            docid = self.index[word[-1]][0]
            docidResult.add(docid)
            for pos in self.findall(word, word[-1]):
                posResult.append((pos, docid))

        for i in xrange(len(word) - 2, -1, -1):
            term = word[i] + word[i + 1]
            if term in self.index:  ## ����Ӧterm����
                for docid in self.index[term]:
                    if not docid in docidResult:  ## ��docδ������(һ��docֻ����һ��term�ĵ�����)
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
                    for pos in posFind:  ##������һ���ǵ�ǰ
                        posResult.append((pos, docid))
        for pos, docid in sorted(posResult, key = lambda posResult: (posResult[0][0], posResult[0][1])):
            result.append((self.docLst[docid], pos))
        return result

    def findall(self, word, doc):
        '''
        ����doc��word�г��ֵ�����λ��
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
    index3.insert(u'����')
    index3.insert(u'��')
    index3.insert(u'����')
    for s, pos in index3.search(u'�벥��������֧����������'):
        print s.encode('gbk', 'ignore'), pos

if __name__ == "__main__":
    main()

        



