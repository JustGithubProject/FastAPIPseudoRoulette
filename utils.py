import random

random_list = ["1$",
               "1$",
               "10$",
               "10$",
               "10$",
               "10$",
               "10$",
               "10$",
               "10$",
               "10$",
               "10$",
               "200$",
               "200$",
               "200$",
               "200$",
               "3000$",
               "4000$",
               "100000000$"
               ]

random.shuffle(random_list)


def spin():
    number = random.choice(random_list)
    return number

