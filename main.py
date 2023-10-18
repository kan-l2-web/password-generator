import random


def create_new(chars, length):
    password = ''

    for _ in range(round(length)):
        password = "".join([password, random.choice(chars)])

    return password
