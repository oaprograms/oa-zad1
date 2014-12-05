__author__ = 'Ognjen Apic'

class User:

    def __init__(self):
        self.id = -1
        self.first_name = u''
        self.last_name = u''
        self.age = -1
        self.gender = u''
        self.friends = set()

    def __str__(self):
        age = str(self.age)
        if self.age < 0:
            age =  ''
        return ';'.join(
            [str(self.id),self.first_name,self.last_name,str(age),self.gender,
             ','.join(str(x) for x in self.friends)])

def parse_user(user_str):
    """ Read user from string formatted: id;first_name;last_name;age;gender;friend1_id,friend2_id...
    :param user_str: string to parse
    :returns: User or None if string format is invalid
    """
    fields = user_str.split(';')
    if len(fields) < 6:
        raise ValueError('too few parameters: ' + user_str)

    (id,first_name,last_name,age,gender,friends_str) = tuple([x.strip() for x in fields[:6]])
    friends = []
    if friends_str:
        friends = [x.strip() for x in friends_str.split(',')]
    # validate fields
    if id.isdigit() \
        and ((not age) or (age.isdigit())) \
        and (gender in ['male', 'female']) \
        and all(x.isdigit() for x in friends):

        # make object
        u = User()
        u.id = int(id)
        u.first_name = first_name
        u.last_name = last_name
        if age:
            u.age = int(age)
        u.gender = gender
        u.friends = set([int(friend) for friend in friends])
        return u
    else:
        raise ValueError('invalid values found in: ' + user_str)
