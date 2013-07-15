#include "AhoCorasick.h"

int AhoCorasick::initialize(int iNumber, const int pLen[], const char* patterns[]) {
	for (int i = 0; i != iNumber; ++i) {  //创建节点
		insert(patterns[i], pLen[i], i);
	}
	fixAhoCorasick();  //填写fail指针
	return 0;
}

int AhoCorasick::release(trieNode* &p) {
	for (std::map<unsigned, trieNode*>::iterator it = p->next.begin(); it != p->next.end(); ++it) {
		release(it->second);
	}
	delete p;
	p = NULL;
	return 0;
}

int AhoCorasick::insert(const char* pattern, int pLen, int patternIndex) {
	if (pLen <= 0) return -1;  //空串不要
	trieNode* p = root;
	for (int i = 0; i != pLen; ++i) { //循环至最底部
		unsigned index = (unsigned char)pattern[i];
		if (p->next.find(index) == p->next.end()) {
			p->next[index] = new trieNode();
		}
		p = p->next[index];
	}
	p->end = true;
	p->pIndex = patternIndex;
	return 0;
}

int AhoCorasick::fixAhoCorasick() {
	std::queue<trieNode*> nodeQueue;
	nodeQueue.push(root);
	while (nodeQueue.size() > 0) {
		trieNode* parent = nodeQueue.front();
		nodeQueue.pop();
		for (std::map<unsigned, trieNode*>::iterator it = parent->next.begin(); it != parent->next.end(); ++it) {
			unsigned index = it->first;
			trieNode* child = it->second;
			if (parent == root) {
				child->fail = root;
			} else {
				trieNode* failp = parent->fail;
				while (failp != NULL) {
					if (failp->next.find(index) != failp->next.end()) {
						child->fail = failp->next[index];
						break;
					}
					failp = failp->fail;
				}
				if (failp == NULL) child->fail = root;
			}
			nodeQueue.push(child);
		}  //for
	}  //while
}

/*
 *匹配子串
 *输入：搜索串str及长度sLen
 *输出：模块串下标及其在str中的位置（最末位）组成的vector
 */
int AhoCorasick::search(const char* str, int sLen, std::vector<std::pair<unsigned, int> >& result) {
	result.clear();
	trieNode* p = root;
	for (int i = 0; i != sLen; ++i) {
		unsigned index = (unsigned char)str[i];
		while (p->next.find(index) == p->next.end() && p != root) {
			p = p->fail;
		}
		if (p->next.find(index) == p->next.end()) {
			p = root;
		} else {
			trieNode* q = p->fail;
			p = p->next[index];
		}
		trieNode *q = p;
		while (q) {
			if (q->end) {
				result.push_back(std::make_pair(q->pIndex, i + 1));
			}
			q = q->fail;
		}
	}
	return 0;
}


