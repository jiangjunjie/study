#!/usr/bin/env python
#coding=gbk

'''
用于合并mspider.blacklist，可选从文件输入或从标准输入
然后在mspider.blacklist后面追加新增
'''

import optparse
import sys

def main():
    parser = optparse.OptionParser()
    parser.add_option('-m', '--merge', help = 'final output file')
    parser.add_option('-a', '--add')
    opt, args = parser.parse_args()
    
    blackDic = {}
    addDic = {}
    fin = open(opt.merge)
    cnt = 0
    k = ''
    v = ''
    for line in fin:
        line = line.rstrip()
        if line.startswith('key:'):
            k = line[4:]
        elif line.startswith('classtag:'):
            cnt += 1
            v = line[9:]
            blackDic[(k, v)] = cnt
        else:
            print >> sys.stderr, line
    fin.close()

    addCnt = cnt    
            
    if opt.add:  ## 合并两文件
        fin = open(opt.add)
        for line in fin:
            line = line.rstrip()
            if line.startswith('key:'):
                k = line[4:]
            elif line.startswith('classtag:'):
                v = line[9:]
                if (k, v) not in blackDic:
                    cnt += 1
                    blackDic[(k, v)] = cnt
                    addDic[(k, v)] = cnt
            else:
                print >> sys.stderr, line
        fin.close()
    else:  ## 从标准输入添加
        for line in sys.stdin:
            line = line.rstrip()
            try:
                k, v = line.split('\t')
                if (k, v) not in blackDic:
                    cnt += 1
                    blackDic[(k, v)] = cnt
                    addDic[(k, v)] = cnt
            except Exception, what:
                print >> sys.stderr, what
                print >> sys.stderr, line
        
    fout = open(opt.merge, 'a')
    for (k, v), cnt in sorted(addDic.items(), key = lambda addDic: addDic[1]):
        print >> fout, 'key:%s' % k
        print >> fout, 'classtag:%s' % v
    fout.close()

if __name__ == "__main__":
    main()
