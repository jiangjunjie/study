#include <iostream>
#include <string>
#include <string.h>
#include <stdlib.h>

#include "Ant.h"
#include "ACOSearch.h"

int Ant::Release() {
	if (_tour_path) {
		delete[] _tour_path;
		_tour_path = NULL;
	}
	if (_visited) {
		delete[] _visited;
		_visited = NULL;
	}
	return 0;
}

int Ant::Init() {
	_added_num = 0;
	_cur_index = -1;
	for (int i = 0; i < _node_num; ++i) {
		_tour_path[i] = -1;
		_visited[i] = false;
	}
	_tour_length = 0;
	return 0;
}

int Ant::Copy(Ant* ant) {
	_node_num = ant->_node_num;
	_added_num = ant->_added_num;
	_cur_index = ant->_cur_index;
	_tour_length = ant->_tour_length;
	for (int i = 0; i < _node_num; ++i) {
		_tour_path[i] = ant->_tour_path[i];
		_visited[i] = ant->_visited[i];
	}
	return 0;
}

// 蚂蚁开始搜索，变量清空及初始化
int ACOSearch::AntInit(Ant* ant) {
	ant->Init();
	int index = rand() % _node_num;
	ant->_cur_index = index;
	ant->_tour_path[ant->_added_num++] = ant->_cur_index;
	ant->_tour_length = 0;
	ant->_visited[index] = true;
	return 0;
}

int ACOSearch::AntSearch(Ant* ant) {
	AntInit(ant);
	int ret = 0;
	while (ant->_added_num < _node_num) {
		ret = AntExpand(ant);
		if (ret != 0) return 1;
	}
	ant->_tour_length += _traffic[ant->_cur_index * _node_num + ant->_tour_path[0]];
	return 0;
}

int ACOSearch::AntExpand(Ant* ant) {
	int ret = 0;
	int node_avail_num = 0;
	double total_prob = 0.0;
	for (int i = 0; i < _node_num; ++i) {
		if (ant->_visited[i]) continue;
		total_prob += _transition_prob[ant->_cur_index * _node_num + i];
		++node_avail_num;
	}

	int next_index = -1;
	if (_next_type == NEXT_TYPE_GREEDY) {
		// 贪心选择下一view
		double max_heuristic = -1;
		for (int i = 0; i < _node_num; ++i) {
			if (ant->_visited[i]) continue;
			if (_heuristic[ant->_cur_index * _node_num + i] > max_heuristic) {
				max_heuristic = _heuristic[ant->_cur_index * _node_num + i];
				next_index = i;
			}
		}
	} else {
		// 轮盘选择
		double random_val = rand() / static_cast<double>(RAND_MAX) * total_prob;
		for (int i = 0; i < _node_num; ++i) {
			if (ant->_visited[i]) continue;
			random_val -= _transition_prob[ant->_cur_index * _node_num + i];
			if (random_val < 0) {
				next_index = i;
				break;
			}
		}
	}
	if (next_index < 0 || next_index >= _node_num) return 1;

	ant->_tour_path[ant->_added_num++] = next_index;
	ant->_tour_length += _traffic[ant->_cur_index * _node_num + next_index];
	ant->_cur_index = next_index;
	ant->_visited[next_index] = true;

	return 0;
}

