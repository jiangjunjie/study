#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ACOSearch.h"

int main(int argc, char **argv) {
	if (argc != 2) {
		fprintf(stderr, "%s eil51.tsp\n", argv[0]);
		return 1;
	}
	std::vector<std::string> city_name_list;
	std::vector<std::pair<int, int> > city_point_list;

	std::ifstream fin(argv[1]);
	std::string line;
	while (std::getline(fin, line)) {
		if (line.size() <= 0 || line.substr(0, 1) == "#") continue;
		std::string::size_type pos = line.find("\t");
		std::string::size_type pos2 = line.rfind("\t");
		if (pos != std::string::npos && pos2 != std::string::npos && pos != pos2) {
			std::string city_name = line.substr(0, pos);
			int point_x = atoi(line.substr(pos + 1, pos2 - pos - 1).c_str());
			int point_y = atoi(line.substr(pos2 + 1).c_str());
			city_name_list.push_back(city_name);
			city_point_list.push_back(std::pair<int, int>(point_x, point_y));
		}
	}
	fin.close();

	int city_num = city_name_list.size();
	std::vector<int> city_dist_list(city_num * city_num, 0);
	for (int i = 0; i < city_num; ++i) {
		for (int j = i + 1; j < city_num; ++j) {
			int dist = (city_point_list[i].first - city_point_list[j].first) * (city_point_list[i].first - city_point_list[j].first) + (city_point_list[i].second - city_point_list[j].second) * (city_point_list[i].second - city_point_list[j].second);
			dist = pow(dist, 0.5) + 0.5;
			city_dist_list[i * city_num + j] = dist;
			city_dist_list[j * city_num + i] = dist;
//			fprintf(stdout, "%d (%d, %d) -> %d (%d, %d): %d\n", i, city_point_list[i].first, city_point_list[i].second, j, city_point_list[j].first, city_point_list[j].second, dist);
		}
	}

	ACOSearch* aco = new ACOSearch;
	aco->DoSearch(city_name_list, city_dist_list);
	for (int i = 0; i < aco->_node_num; ++i) {
		fprintf(stdout, "%d", aco->_best_ant->_tour_path[i]);
		if (i == 0) {
			fprintf(stdout, "\t0\n");
		} else {
			int cur_index = aco->_best_ant->_tour_path[i];
			int last_index = aco->_best_ant->_tour_path[i - 1];
			fprintf(stdout, "\t%d\n", aco->_traffic[last_index * aco->_node_num + cur_index]);
		}
	}
	fprintf(stdout, "%d\n", aco->_best_ant->_tour_length);
	delete aco;

	return 0;
}

