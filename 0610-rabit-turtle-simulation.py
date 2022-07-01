from base import *
import random
import time

LENGTH_OF_RACE = 1000

class turtle:
    def __init__(self):
        global LENGTH_OF_RACE
        self.name = "turtle"
        self.speed = 4
        self.current_position = 0
        self.LENGTH_OF_RACE = LENGTH_OF_RACE

    def step(self):
        self.current_position += self.speed
        if self.current_position > self.LENGTH_OF_RACE:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.name}:currently at {self.current_position}, speed: {self.speed}, {round(self.current_position/self.LENGTH_OF_RACE * 100, 2)}% complete"

class rabbit:
    def __init__(self):
        global LENGTH_OF_RACE
        self.name = "rabbit"
        self.speed = 0
        self.current_position = 0
        self.wake_between_nap = random.randint(0,10)
        self.duration_of_nap = random.randint(0,200)
        self.since_last_wake = 0
        self.is_nasleeping = False
        self.since_last_nap = 0
        self.LENGTH_OF_RACE = LENGTH_OF_RACE

    def step(self):
        if self.since_last_wake >= self.wake_between_nap:
            self.is_nasleeping = True
        if self.since_last_nap >= self.duration_of_nap:
            self.is_nasleeping = False
        if self.is_nasleeping:
            self.since_last_nap = 0
            self.since_last_wake += 1
        else:
            self.since_last_wake = 0
            self.since_last_nap += 1
            self.speed = random.randint(4, 8)
            self.current_position += self.speed
        if self.current_position > self.LENGTH_OF_RACE:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.name}:currently at {self.current_position}, speed: {self.speed}, {round(self.current_position/self.LENGTH_OF_RACE * 100, 2)}% complete, {'sleeping'}"

if __name__ == '__main__':
    rabbit_0 = rabbit()
    turtle_0 = turtle()
    stat = False
    step = 0
    while stat is False:
        step += 1
        stat = rabbit_0.step() | turtle_0.step()
        log.debug(step, rabbit_0, turtle_0)
        print(step, rabbit_0, turtle_0)
