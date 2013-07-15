/**
  *@��STL map�� transition function ��Aho-Corasick Automatonʵ��
  *@��array��ȣ���ʡ�˿ռ䣬������������ʱ��
  *@bug����unicode�Զ�����ͨ����ĳЩ����ģʽ���ᱻƥ�䣬ex:ģʽ��"��"�� ������"������"
  *@author Jiang Junjie
  *@date 2013-07-05
  */
#ifndef _AHOCORASICK_H_
#define _AHOCORASICK_H_
#include <map>
#include <queue>

class AhoCorasick {
public:
	AhoCorasick() {
		root = new trieNode();
	}
	~AhoCorasick() {
		release(root);
	}

	int search(const char* str, int sLen, std::vector<std::pair<unsigned, int> >& result);
	int initialize(int iNumber, const int pLen[], const char* patterns[]);

private:
	struct trieNode {
		trieNode* fail;
		std::map<unsigned, trieNode*> next;
		bool end;
		unsigned pIndex;  //�ڼ���pattern
		trieNode() {
			fail = NULL;
			end = false;
		}
	};
	trieNode* root;

private:
	int insert(const char* pattern, int pLen, int patternIndex);
	int fixAhoCorasick();
	int release(trieNode* &p);
};


#endif  // AhoCorasick.h
