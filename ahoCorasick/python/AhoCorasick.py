#!/usr/bin/env python
#coding=gbk

'''
��hashmapʵ��AC�Զ�����֧������Ϊunicode�����õ�ƥ�䵥������pattern
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
        ����query
        '''
        word = word.strip()  ## �մ�����
        if not word:
            return
        p = self.root  ## pָ��root
        for w in word:  ## ѭ��ÿ����
            if w in p.next:  ## ����Ѳ������ָ����
                p = p.next[w]
            else:  ## �������½ڵ㣬ָ���½ڵ�
                q = Node()  ##�½ڵ�
                p.next[w] = q
                p = q
        p.word = word  ## ���е��ʶ������˽�㣬��ĩ��㴦дword��end
        p.end = True

    def fix(self):
        '''
        ����failָ��
        '''
        self.root.fail = None
        queue = [self.root]  ## ������ȱ���������ָ�������
        while len(queue) != 0:
            parent = queue[0]
            queue.pop(0)  ## ����������
            for w in parent.next:  ## ����ÿ������
                child = parent.next[w]
                failp = parent.fail
                while failp != None:
                    if w in failp.next:  ## �Ҹ�����failָ�룬�����Ƿ��е�ǰ���ӣ������ָ�򼴿�
                        child.fail = failp.next[w]
                        break
                    failp = failp.fail  ## ���򲻶��Ҹ�����failָ��
                if failp == None:  ## �������ָ��root��˵���޷��ҵ�����ǰ���ӵ�failָ��root
                    child.fail = self.root
                queue.append(child)  ## ����������У�������ȴ���

    def search(self, word):
        '''
        ��������ƥ���Ӵ�
        '''
        result = []
        p = self.root  ## �Ӹ���㿪ʼ����
        for i, w in enumerate(word):  ## ������ָ�벻����ǰ������
            while p != None and not w in p.next:  ## �����ǰ��㲻���ڸõ��ʣ�����failָ���Ƿ���ڸõ���
                p = p.fail
            if p == None:  ## ���ݹ�root�ڵ��ˣ�˵��û���ҵ�����pָ��root
                p = self.root
            else:  ## ����˵���ҵ��ˣ�pָ��Ϊ�õ��ʵĽ��
                p = p.next[w]
            q = p  ## �жϸõ��ʽ�㼰��һ����fail����Ƿ���ĳ��pattern��ĩβ
            while q != None:
                if q.end:  ## ����ǣ����ظ�ģʽ�������ɼ������ģʽ���������е�ͷβλ��
                    result.append(((i + 1 - len(q.word), i + 1), q.word))
                q = q.fail  ## ����Ѱ��fail��㣬ֱ�����ݹ�root
        return result

def main():
    aho = AhoCorasick()
    patternLst = [u'����', u'��', u'����']
    ms = u'�첥��������'
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
