__author__ = 'Ognjen Apic'
import codecs
import user

class UserGraph:

    def __init__(self, user_dict):
        UserGraph.validate_users(user_dict)
        self.users = user_dict

    @staticmethod
    def validate_users(user_dict):
        """Ensures that friendships are bidirectional and that all ids exist
        """
        for id,user in user_dict.iteritems():
            for friend_id in user.friends:
                if (friend_id not in user_dict) or (id not in user_dict[friend_id].friends):
                    raise Exception('validate_users failed')

    def is_friend(self, id1, id2):
        """See if two users are friends
            Friend ids are stored in a set, so O(n) is constant
        """
        if id1 in self.users and id2 in self.users:
            return id2 in self.users[id1].friends
        else:
            raise ValueError('invalid user id')

    def shortest_distance(self, id1, id2):
            """Computes the shortest friendship path between two users
            :returns: list of friend-of-friend's ids that are traversed, including id2
            """
            # check for direct friendship
            if self.is_friend(id1,id2):
                return [id2]

            # structure for keeping track of ids for two sides of the search
            # (from start [id1], and from destination [id2])
            # these are swapped during search, so we keep them in the list [s],
            # that will be reversed when search direction is changed
            s = [
                {'found': {id1:None}, 'old': set(), 'dead_end': False},
                {'found': {id2:None}, 'old': set(), 'dead_end': False}
            ]
            # 'found': found ids and their previous friend's ids (that lead to search ends)
            # 'old': keeping track of traversed ids, to speed things up
            # 'dead_end': if we traversed whole isolated sub-graph, prevents infinite loop
            #             (probably not gonna happen often)

            if id2 in self.users[id1].friends:
                return [id2]

            search_left = True

            # in a graph, expand left search area, then right search area, so on, until an overlap is detected
            while(not ((s[0]['dead_end']) and (s[1]['dead_end']))):
                found_new = False # to keep track of dead ends
                for id in s[0]['found'].keys():
                    if id not in s[0]['old']: # for every new, non-traversed key:
                        s[0]['old'].add(id)
                        for friend_id in self.users[id].friends:
                            if friend_id not in s[0]['found']:  # for every new friend
                                # check if friend is in the other end's circle:
                                if friend_id in s[1]['found']:
                                    # we made it. reconstruct path lists and return it:
                                    ret_list = []
                                    while(s[1]['found'][friend_id] != None):
                                        ret_list = [friend_id] + ret_list
                                        friend_id = s[1]['found'][friend_id]
                                    while(s[0]['found'][id] != None):
                                        ret_list.append(id)
                                        id = s[0]['found'][id]
                                     # how we return the list depends on the last search direction:
                                    if search_left:
                                        ret_list = [friend_id] + ret_list
                                        ret_list.reverse()
                                        return ret_list
                                    else:
                                        return ret_list + [id]
                                else:
                                #   if no, add friend to the circle
                                    s[0]['found'][friend_id] = id
                                    found_new = True
                s[0]['dead_end'] = not found_new
                search_left = not search_left
                s.reverse()
            # if while ended, there is no path between users
            return None

    def shortest_distance_old(self, id1, id2):
        """ WARNING: This is previous, less efficient solution

            Computes the shortest friendship path between two users
            :returns: list of friend-of-friend's ids that are traversed
        """
        # check for direct friendship
        if self.is_friend(id1,id2):
            return [id2]

        left_search_ids = {id1:[]}
        right_search_ids = {id2:[]}

        left_searched_ids = set()
        right_searched_ids = set()

        if id2 in self.users[id1].friends:
            return [id2]

        search_left = True
        left_dead_end = False
        right_dead_end = False
        # in a graph, expand left search area, then right search area, so on, until an overlap is detected
        while(not (left_dead_end and right_dead_end)):
            if search_left:
                found_new = False
                for id in left_search_ids.keys():
                    if id not in left_searched_ids:
                        left_searched_ids.add(id)
                        for friend_id in self.users[id].friends:
                            if friend_id not in left_search_ids:
                                # check if friend_id is in right_search_ids:
                                if friend_id in right_search_ids:
                                #   if yes, return result (merge corresponding path lists)
                                    return left_search_ids[id] + right_search_ids[friend_id] + [id2]
                                else:
                                #   if no, add it to the list
                                    left_search_ids[friend_id] = left_search_ids[id] + [friend_id]
                                    found_new = True
                left_dead_end = not found_new
                search_left = False
            else: # search right
                found_new = False
                for id in right_search_ids.keys():
                    if id not in right_searched_ids:
                        right_searched_ids.add(id)
                        for friend_id in self.users[id].friends:
                            if friend_id not in right_search_ids:
                                # check if friend_id is in left_search_ids:
                                if friend_id in left_search_ids:
                                #   if yes, return result (merge corresponding path lists)
                                    return left_search_ids[friend_id] +  right_search_ids[id] + [id2]
                                else:
                                #   if no, add it to the list
                                    right_search_ids[friend_id] = [friend_id] + right_search_ids[id]
                                    found_new = True
                right_dead_end = not found_new
                search_left = True
        # if while ended, there is no path between users
        return None


def read_file(file_name):
    """ Read CSV file containing users
        :param file_name: input file name
        :returns: dictionary with user ids as keys, and User objects as values
    """
    dict = {}
    # read file, split lines
    with codecs.open(file_name, "r", "utf-8") as f:
        lines = f.read().split('\n')
        for line in lines:
            if line.strip():
                try:
                    # parse user
                    u = user.parse_user(line)
                    # put it in dictionary
                    dict[u.id] = u
                except ValueError, e:
                    print 'Error: ' + str(e) # just print and continue
        return UserGraph(dict)