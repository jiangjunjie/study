#ifndef __ANT_H__
#define __ANT_H__

#include <iostream>
#include <tr1/unordered_set>


class Ant {
public:
	Ant(int node_num) {
		_node_num = node_num;
		_tour_path = new int[_node_num];
		_visited = new bool[_node_num];
		for (int i = 0; i < _node_num; ++i) {
			_tour_path[i] = -1;
			_visited[i] = false;
		}
		
	}
	virtual ~Ant() {
		Release();
	}
	int Copy(Ant* ant);
	int Init();
	int Release();
public:
	int _node_num;
	int _added_num;
	int* _tour_path;
	int _tour_length;
	bool* _visited;
	int _cur_index;
};

#endif
