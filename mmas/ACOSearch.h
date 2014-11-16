#ifndef _ACOSEARCH_H_
#define _ACOSEARCH_H_

#include <vector>

#include "Ant.h"

enum NEXT_TYPE {
	NEXT_TYPE_GREEDY,  // 贪心
	NEXT_TYPE_WHEEL  // 轮盘
};

class ACOConfig {
public:
	ACOConfig() {
		_alpha = 1;
		_beta = 3;  // 当允许迭代次数很多时，可以取1，消弱启发函数的作用，否则，取侧重启发函数，快速达到局部最优
		_rho = 0.98;  // 残留因子
		_iter_num = 100000;
		_min_convergence_num = 200;  // 最优解收敛次数
		_min_ant_num = 10;
		_max_ant_num = 50;
		_pbest = 0.05;
	}
public:
	int _alpha;
	int _beta;
	double _rho;
	int _iter_num;
	int _min_convergence_num;
	int _min_ant_num;
	int _max_ant_num;
	double _pbest;
};


class ACOSearch {
public:
	ACOSearch() {
		_ants = NULL;
		_pheromone = NULL;
		_traffic = NULL;
		_heuristic = NULL;
		_transition_prob = NULL;
		_next_type = NEXT_TYPE_WHEEL;
		_pheromone_init = false;
	}
public:
	virtual ~ACOSearch() {
		Release();
	}
	int Release();
	int SetConfig(ACOConfig& config) {
		_config = config;
		return 0;
	}
	int DoSearch(std::vector<std::string>& city_name_list, std::vector<int>& city_dist_list);
	int Init(std::vector<std::string>& city_name_list, std::vector<int>& city_dist_list);
	int PrepareSearch();
	int Search();
	int UpdatePheromone(Ant* update_ant);
	int UpdateTranProb();
	
	int AntSearch(Ant* ant);
	int AntInit(Ant* ant);
	int AntExpand(Ant* ant);
	
public:
	ACOConfig _config;

	int _node_num;  // 节点数，包括景点不同段内重复
	
	double* _pheromone;
	int* _traffic;
	double* _heuristic;
	double* _transition_prob;
	
	int _ant_num;
	Ant** _ants;	
	Ant* _best_ant;
	
	int _convergence_num; // 最佳路线迭代稳定次数

	int _next_type;  // 下一节点的筛选方法?贪心:轮盘

	double _pheromone_max_min_times;

	bool _pheromone_init;
};


#endif
