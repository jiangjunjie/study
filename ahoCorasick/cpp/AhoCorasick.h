/**
  *@用STL map作 transition function 的Aho-Corasick Automaton实现
  *@与array相比，节省了空间，但增加了搜索时间
  *@bug：非unicode自动机的通病，某些单字模式串会被匹配，ex:模式串"牌"， 搜索串"播放器"
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
		unsigned pIndex;  //第几个pattern
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
