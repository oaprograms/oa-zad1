#!/usr/bin/python
__author__ = 'Ognjen Apic'

import user_graph

if __name__ == "__main__":
    users = user_graph.read_file('data.txt')
    print users.shortest_distance(18,1)