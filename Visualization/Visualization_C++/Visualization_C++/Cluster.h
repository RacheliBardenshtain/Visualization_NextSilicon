#pragma once
#include <iostream>

using namespace std;

class Cluster {
public:
	int chip;
	int die;
	int quad;
	int row;
	int col;

	Cluster(int chip, int die, int quad, int row, int col) :chip(chip), die(die), quad(quad), row(row), col(col) {

	}

	Cluster() {

	}

	bool operator==(const Cluster& other) const {
		return chip == other.chip && die == other.die && quad == other.quad && row == other.row && col == other.col;
	}

	friend ostream& operator<<(ostream& os, const Cluster& cluster) {
		os << "chip:" << cluster.chip << ", die:" << cluster.die << ", quad:" << cluster.quad << ", row:" << cluster.row << ", col:" << cluster.col;
		return os;
	}
};

namespace std {
	template <>
	struct hash<Cluster> {
		size_t operator()(const Cluster& c) const {
			size_t h1 = hash<int>{}(c.die);
			size_t h2 = hash<int>{}(c.quad);
			size_t h3 = hash<int>{}(c.row);
			size_t h4 = hash<int>{}(c.col);
			size_t h5 = hash<int>{}(c.chip);
			return h1 ^ (h2 << 1) ^ (h3 << 2) ^ (h4 << 3) ^ (h5 << 4);
		}
	};
}
