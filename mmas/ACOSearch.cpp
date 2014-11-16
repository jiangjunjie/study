#include "ACOSearch.h"
#include <algorithm>
#include <limits>
#include <math.h>
#include <stdio.h>
#include <time.h>

int ACOSearch::Release() {
	if (_ants) {
		for (int i = 0; i < _ant_num; ++i) {
			delete _ants[i];
		}
		delete[] _ants;
		_ants = NULL;
	}
	if (_best_ant) {
		delete _best_ant;
		_best_ant = NULL;
	}
	if (_pheromone) {
		delete[] _pheromone;
		_pheromone = NULL;
	}
	if (_traffic) {
		delete[] _traffic;
		_traffic = NULL;
	}
	if (_heuristic) {
		delete[] _heuristic;
		_heuristic = NULL;
	}
	if (_transition_prob) {
		delete[] _transition_prob;
		_transition_prob = NULL;
	}
	return 0;
}

// 初始化数据
int ACOSearch::Init(std::vector<std::string>& city_name_list, std::vector<int>& city_dist_list) {
	_node_num = city_name_list.size();

	// 交通及启发函数
	_traffic = new int[_node_num * _node_num];
	_heuristic = new double[_node_num * _node_num];
	for (int i = 0; i < _node_num * _node_num; ++i) {
		_traffic[i] = city_dist_list[i];
		_heuristic[i] = 0.0;
		if (_traffic[i] > 0) {
			_heuristic[i] = pow(1.0 / _traffic[i], _config._beta);
		}
	}
	
	// 信息素
	_pheromone = new double[_node_num * _node_num];
	_pheromone_max_min_times = (1 - pow(_config._pbest, 1.0 / _node_num) ) / (_node_num / 2.0 - 1) / pow(_config._pbest, 1.0 / _node_num);

	// 转移概率
	_transition_prob = new double[_node_num * _node_num];

	// 蚂蚁
	_ant_num = 2 * _node_num / 3 + 1;
	_ants = new Ant*[_ant_num];
	for (int k = 0; k < _ant_num; ++k) {
		Ant* ant = new Ant(_node_num);
		_ants[k] = ant;
	}
	_best_ant = new Ant(_node_num);
	_best_ant->_tour_length = std::numeric_limits<int>::max();

	// 随机数种子
//	srand((unsigned)time(0));
	srand(1416140184);  // 426所用种子
	return 0;
}


int ACOSearch::DoSearch(std::vector<std::string>& city_name_list, std::vector<int>& city_dist_list) {
	int ret = 0;

	// Step 1 初始化
	Init(city_name_list, city_dist_list);

	// Step 2 搜索前中变量填值
	PrepareSearch();
	
	// Step 3 开始拓展
	Search();

	return ret;
}

// 成员初始化
int ACOSearch::PrepareSearch() {
	for (int i = 0; i < _node_num * _node_num; ++i) {
		_pheromone[i] = 1.0;
	}
	for (int i = 0; i < _node_num * _node_num; ++i) {
		_transition_prob[i] = 0.0;
	}
	UpdateTranProb();

	_best_ant->_tour_length = std::numeric_limits<int>::max();

	_next_type = NEXT_TYPE_GREEDY;
	return 0;
}

// 搜索路径
int ACOSearch::Search() {
	_pheromone_init = false;
	_convergence_num = 0;
	for (int iter = 0; iter < _config._iter_num; ++iter) {
		Ant* best_ant_iter = NULL;  // 每次迭代最优蚂蚁
		for (int k = 0; k < _ant_num; ++k) {
			if (iter == 0 && k == 0) {
				_next_type = NEXT_TYPE_GREEDY;
			} else {
				_next_type = NEXT_TYPE_WHEEL;
			}
			AntSearch(_ants[k]);
//			fprintf(stderr, "ACOSearch::Search, iter: %d, ant: %d, Search success, length: %d, best: %d\n", iter, k, _ants[k]->_tour_length, _best_ant->_tour_length);
			if (best_ant_iter == NULL) best_ant_iter = _ants[k];
			if (_ants[k]->_tour_length < best_ant_iter->_tour_length) {
				best_ant_iter = _ants[k];
			}
			// 第一个成功就退出，填写初始信息素
			if (!_pheromone_init) break;
		}  // for _ant_num

		fprintf(stderr, "ACOSearch::Search, iter: %d, best_length: %d, best_iter: %d\n", iter, _best_ant->_tour_length, best_ant_iter->_tour_length);
		
		// 判断收敛
		if (best_ant_iter->_tour_length < _best_ant->_tour_length) {
			_best_ant->Copy(best_ant_iter);
			_convergence_num = 1;
		} else {
			++_convergence_num;
		}
		// 收敛直接退出迭代
		if (_convergence_num >= _config._min_convergence_num) {
			fprintf(stderr, "ACOSearch::Search, iter: %d, SearchPath Convergence! best_length: %d\n", iter, _best_ant->_tour_length);
			break;
		}
		// 选择更新蚂蚁?全局最优:局部最优
		Ant* update_ant = NULL;
		if (0) {
			update_ant = _best_ant;
		} else {
			update_ant = best_ant_iter;
		}

		// 更新信息素及转移概率
		UpdatePheromone(update_ant);
	}  // for iter
	return 0;
}

// 每次迭代后更新信息素
int ACOSearch::UpdatePheromone(Ant* update_ant) {
	double pheromone_max = 1.0 / _best_ant->_tour_length / (1.0 - _config._rho);
	double pheromone_min = pheromone_max * _pheromone_max_min_times;
//	fprintf(stderr, "ACOSearch::UpdatePheromone, pheromone_max: %.8f, pheromone_min: %.10f, best_length: %d\n", pheromone_max, pheromone_min, _best_ant->_tour_length);

	if (!_pheromone_init) {
		// 第一次贪心，信息素未初始化
		for (int i = 0; i < _node_num * _node_num; ++i) {
			_pheromone[i] = pheromone_max;
		}
		_pheromone_init = true;
	} else {
		// 信息素挥发
		for (int i = 0; i < _node_num; ++i) {
			for (int j = 0; j < _node_num; ++j) {
				_pheromone[i * _node_num + j] *= _config._rho;  // rho为残留因子
			}
		}
		// 信息素增加
		double update_pheromone = 1.0 / update_ant->_tour_length;
		int last_index = update_ant->_tour_path[0];
		for (int s = 1; s < update_ant->_added_num; ++s) {
			int index = update_ant->_tour_path[s];
			_pheromone[last_index * _node_num + index] += update_pheromone;
			last_index = index;
		}
	}

	// 信息素阈值
	for (int i = 0; i < _node_num; ++i) {
		for (int j = 0; j < _node_num; ++j) {
			if (_pheromone[i * _node_num + j] > pheromone_max) {
				_pheromone[i * _node_num + j] = pheromone_max;
			} else if (_pheromone[i * _node_num + j] < pheromone_min) {
				_pheromone[i * _node_num + j] = pheromone_min;
			}
		}
	}

	// 更新转移概率
	UpdateTranProb();

	return 0;
}

// 每次更新信息素之后须更新转移概率
int ACOSearch::UpdateTranProb() {
	for (int i = 0; i < _node_num; ++i) {
		for (int j = 0; j < _node_num; ++j) {
			if (i == j) continue;
			_transition_prob[i * _node_num + j] = pow(_pheromone[i * _node_num + j], _config._alpha) * _heuristic[i * _node_num + j];
		}
	}
	return 0;
}

