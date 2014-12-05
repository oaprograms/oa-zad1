#!/usr/bin/python
__author__ = 'Ognjen'

import user
import user_graph
import unittest

class UserTest(unittest.TestCase):

    def setUp(self):
        self.user_strings = ["1;Paul;Crowe;28;male;2",
                      "2;Rob;Fitz;23;male;1,3",
                      "3;Ben;O'Carolan;;male;2,4",
                      "4;Victor;;28;male;3",
                      "5;Peter;Mac;29;male;"
                          ]

    def test_users(self):
        users = [user.parse_user(x) for x in self.user_strings]
        # test __str__
        self.assertEqual([str(u) for u in users], self.user_strings)
        # test user graph
        dict = {u.id:u for u in users}
        graph = user_graph.UserGraph(dict)
        self.assertEqual(graph.shortest_distance(1,2), [2])
        self.assertEqual(graph.shortest_distance(1,4), [2,3,4])
        self.assertEqual(graph.shortest_distance(4,1), [3,2,1])
        self.assertEqual(graph.shortest_distance(5,1), None)
        # test shortest_distance2
        #for i in range(1,6):
        #    for j in range(1,6):
        #        self.assertEqual(graph.shortest_distance(i,j), graph.shortest_distance2(i,j))
        # test friends
        self.assertEqual(graph.is_friend(1,2), True)
        self.assertEqual(graph.is_friend(1,3), False)

        graph2 = user_graph.read_file('data.txt')
        for i in range(1,20):
            for j in reversed(range(1,20)):
                self.assertEqual(graph2.shortest_distance(i,j), graph2.shortest_distance_old(i,j))
                #print str(i) + ';' + str(j) + ';' + str(graph2.shortest_distance(i,j))


if __name__ == '__main__':
    unittest.main()