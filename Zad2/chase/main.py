import random
import math
import json
import csv

class Sheep:
    def __init__(self, sheep_move, init_pos_limit):
        self.id = id
        self.sheep_move = sheep_move
        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.alive = True

    def move(self):
        if self.alive:
            direction = random.randint(1, 4)
            if direction == 1:
                self.y = self.y + self.sheep_move
            elif direction == 2:
                self.x = self.x + self.sheep_move
            elif direction == 3:
                self.y = self.y - self.sheep_move
            elif direction == 4:
                self.x = self.x - self.sheep_move




class Wolf:
    def __init__(self, wolf_move, sheep):
        self.x = 0.0
        self.y = 0.0
        self.wolf_move = wolf_move
        self.sheep = sheep
        self.last = None

    def move(self):
        nearest = self.check_nearest_sheep()
        if self.check_if_caught(nearest):
            self.x = nearest.x
            self.y = nearest.y
            nearest.alive = False
            self.last = nearest
        else:
            if nearest.x >= self.x:
                self.x = self.x + self.wolf_move * abs(
                    self.x - nearest.x) / self.calculate_distance(nearest)
            else:
                self.x = self.x - self.wolf_move * abs(
                    self.x - nearest.x) / self.calculate_distance(nearest)
            if nearest.y >= self.y:
                self.y = self.y + self.wolf_move * abs(
                    self.y - nearest.y) / self.calculate_distance(nearest)
            else:
                self.y = self.y - self.wolf_move * abs(
                    self.y - nearest.y) / self.calculate_distance(nearest)

    def check_nearest_sheep(self):
        y = True
        z = 0
        dist = None
        sheep = None
        while y:
            if self.sheep[z].alive:
                dist = self.calculate_distance(self.sheep[z])
                sheep = self.sheep[z]
                y = False
            z = z + 1
        for x in self.sheep:
            if x.alive:
                if dist >= self.calculate_distance(x):
                    dist = self.calculate_distance(x)
                    sheep = x
        return sheep

    def check_if_caught(self, sheep):
        if self.calculate_distance(sheep) < self.wolf_move:
            return True
        else:
            return False

    def calculate_distance(self, sheep):
        return math.sqrt(
            (self.x - sheep.x) ** 2 + (self.y - sheep.y) ** 2)



# initialize csv lists
header = ["Round number", "Number of alive sheep"]
data = []

# initialize json list
dictionaries = []

# initialize variable
sheep_list = []
maximum_number_of_rounds = 50
the_number_of_sheep = 15
init_pos_limit = 10.0
sheep_move = 0.5
wolf_move = 1.0

# creating wolf and sheeps
for x in range(the_number_of_sheep):
    sheep_list.append(Sheep(sheep_move, init_pos_limit))
    sheep_list[x].id = x
wo = Wolf(wolf_move, sheep_list)

# started values
number_of_alive = 0
for sheep in sheep_list:
    if sheep.alive:
        number_of_alive = number_of_alive + 1
print("Started values: ")
print("Wolf position: (", round(wo.x, 3), ",", round(wo.y, 3), ")")
print("Number of alive sheep: ", number_of_alive)
print("Id of the closest sheep: ", wo.check_nearest_sheep().id)

# create dictionary for json and adding it to variable
sheep_position_list = []
for sheep in sheep_list:
    if sheep.alive:
        sheep_position_list.append([sheep.x, sheep.y])
    else:
        sheep_position_list.append(None)
dictionary = {
    "round_no": 0,
    "wolf_pos": [wo.x, wo.y],
    "sheep_pos": sheep_position_list
}
dictionaries.append(dictionary)

# adding row to data csv
row = [0, number_of_alive]
data.append(row)

# main code
number_of_death_sheep_round_ago = 0
for x in range(maximum_number_of_rounds):
    print("\nRound: ", x + 1)
    number_of_alive_sheep_before_move = 0
    for sheep in sheep_list:
        if sheep.alive:
            number_of_alive_sheep_before_move = number_of_alive_sheep_before_move + 1
    if number_of_alive_sheep_before_move > 0:
        for sheep in sheep_list:
            sheep.move()
        wo.move()
        number_of_alive_sheep_after_move = 0
        for sheep in sheep_list:
            if sheep.alive:
                number_of_alive_sheep_after_move = number_of_alive_sheep_after_move + 1
        print("Wolf position: (", round(wo.x, 3), ",", round(wo.y, 3), ")")
        print("Number of alive sheep: ", number_of_alive_sheep_after_move)
        if number_of_alive_sheep_after_move > 0:
            print("Id of the closest sheep: ", wo.check_nearest_sheep().id)
        if the_number_of_sheep - number_of_alive_sheep_after_move > number_of_death_sheep_round_ago:
            number_of_death_sheep_round_ago += 1
            print("Id of sheep caught in last round: ", wo.last.id)

        # create dictionary for json and adding it to variable
        sheep_position_list = []
        for sheep in sheep_list:
            if sheep.alive:
                sheep_position_list.append([sheep.x, sheep.y])
            else:
                sheep_position_list.append(None)
        dictionary = {
            "round_no": x + 1,
            "wolf_pos": [wo.x, wo.y],
            "sheep_pos": sheep_position_list
        }
        dictionaries.append(dictionary)

        # adding row to data csv
        row = [x + 1, number_of_alive_sheep_after_move]
        data.append(row)
    else:
        print("Every sheep are caught!")
        break

# saving to json
json_object = json.dumps(dictionaries, indent=3)
with open("pos.json", "w") as outfile:
    outfile.write(json_object)

# saving to csv
with open('alive.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)
