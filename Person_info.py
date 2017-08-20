#! /usr/bin/python

import sys


required_data = ('name', 'surname', 'sex (M/F)', 'age (full years)')
question = 'Insert person'
stop_word = 'Enough'


def insert_data(param, val):
    return input('{} {}: '.format(param, val))


def process_input_data():
    data = {}
    stop = False
    for val in required_data:
        data[val] = insert_data(question, val)
        while True:
            if not data[val]:
                data[val] = insert_data(question, val)
            else:
                break
        if val == required_data[0] and data[val] == stop_word:
            stop = True
            break
        if val == required_data[2]:
            while True:
                if data[val].upper() not in ['M', 'F']:
                    print('Please, insert M or F value ')
                    data[val] = insert_data(question, val).upper()
                else:
                    break
        if val == required_data[3]:
            while True:
                if not data[val].isnumeric():
                    print('Age should be integer number\n')
                    data[val] = insert_data(question, val)
                elif int(data[val]) < 0:
                    print('Age cannot be negative.\n')
                    data[val] = insert_data(question, val)
                else:
                    break

    return data, stop


class Person(object):

    def __init__(self, name, surname, sex=False, age=0):
        self.name = name
        self.surname = surname
        self.sex = sex
        self.age = age

    def show_person_data(self):
        print('---------Person Info-------------')
        print('Person name: {}'.format(self.name))
        print('Person surname: {}'.format(self.surname))
        print('Person sex: {}'.format('Male' if self.sex is True else 'Female'))
        print('Person age: {} full years'.format(self.age))
        print('---------------------------------')


if __name__ == '__main__':
    persons_db = []
    while True:
        data_dict, stop_execution = process_input_data()
        if not stop_execution:
            persons_db.append(Person(data_dict[required_data[0]],
                                     data_dict[required_data[1]],
                                     True if data_dict[required_data[2]].upper() == 'M' else False,
                                     data_dict[required_data[3]]))
        else:
            for person in persons_db:
                person.show_person_data()
            sys.exit('You have completed the script.')
