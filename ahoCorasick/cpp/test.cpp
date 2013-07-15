#include "AhoCorasick.h"
#include <iostream>

int main(int argc, char **argv) {
	char** keys = new char*[2];
	int* lens = new int[2];
	keys[0] = new char[10];
	keys[1] = new char[10];

	strcpy(keys[0], "abc");
	lens[0] = strlen("abc");
	keys[0][lens[0]] = '\0';

	strcpy(keys[1], "cd");
	lens[1] = strlen("cd");
	keys[1][lens[1]] = '\0';

	AhoCorasick aho;
	aho.initialize(2, lens, (const char**)keys);

	std::vector<std::pair<unsigned, int> > result;
	aho.search("123abcdef", 9, result);
	for (std::vector<std::pair<unsigned, int> >::iterator it = result.begin(); it != result.end(); ++it) {
		fprintf(stdout, "[%s]\t[%d]\t[%d]\n", keys[it->first], it->second - lens[it->first], it->second);
	}

	delete[] keys[0];
	delete[] keys[1];
	delete[] keys;
	delete[] lens;

	return 0;
}

