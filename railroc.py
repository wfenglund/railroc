# input: a text-file containing possible hubs with car holding limit with possible cars with
# possible states [cargo/people 0/1/2] (0 == empty, 1 == full, 2 == either)
# example row:
# hub1|2;car1|cargo 0,car2|people 1

import random

def generate_placements(in_dict, limit_dict):
    hub_dict = {k: [] for k in list(in_dict)}
    key_list = [list(i[1]) for i in in_dict.items()]
    car_set = set([i for j in key_list for i in j])
    car_list = list(car_set)
    limit_values = [int(i) for i in limit_dict.values()]
    if len(car_list) > sum(limit_values):
        return "Too Many Cars"
    for car in car_list:
        filt_dict = dict(filter(lambda pair : car in pair[1],
                                in_dict.items())) # only look at hubs that can hold the car
        filt_dict = dict(filter(lambda pair : int(limit_dict[pair[0]]) > len(hub_dict[pair[0]]),
                                filt_dict.items())) # only look at hubs that has room
        hub_key, i = random.choice(list(filt_dict.items()))
        hub_dict[hub_key] = hub_dict[hub_key] + [car]
    return hub_dict

def print_placements(in_dict):
    hub_list = list(in_dict)
    for hub in hub_list:
        print(f'{hub}:\n{in_dict[hub]}')
    print()

def merge_dicts(dict1, dict2):
    dict3 = dict1.copy()
    dict3.update(dict2)
    return dict3

def parse_input(input_file):
    hub_dict = {}
    limit_dict = {}
    with open(input_file) as file:
        for line in file:
            hub_string, hub_info = line.split(';')
            car_dict = {}
            for car_entry in hub_info.strip().split(','):
                car = car_entry.split('|')
                car_dict[car[0]] = car[1]
            hub_name, hub_limit = hub_string.split('|')
            limit_dict[hub_name] = hub_limit
            if hub_name in list(hub_dict): # if this is not the first entry of this hub
                hub_dict[hub_name] = merge_dicts(car_dict, hub_dict[hub_name])
            else:
                hub_dict[hub_name] = car_dict
    return hub_dict, limit_dict

def generate_operation(in_dict, placements_dict, limit_dict):
    # Pick a location to move a car from:
    filt_dict = dict(filter(lambda pair : len(placements_dict[pair[0]]) > 0, in_dict.items()))
    hub1, car_dict1 = random.choice(list(filt_dict.items()))
    # Pick a car to move from the location:
    car1 = random.choice(placements_dict[hub1])
    meta1 = car_dict1[car1]
    type1, nmbr = meta1.split() # type1 is not used
    state1 = 'empty' if nmbr == '0' else 'full' if nmbr == '1' else random.choice(['empty', 'full'])
    # Pick a destination to move the car to:
    filt_dict = dict(filter(lambda pair : car1 in pair[1], in_dict.items()))
    filt_dict.pop(hub1)
    hub2, car_dict2 = random.choice(list(filt_dict.items())) # car_dict2 is not used
    print(f'We need you to bring the {state1} {car1} from the {hub1} to the {hub2}.')
    # Check if the destination has room. If not, select a car to move to another location:
    if (int(limit_dict[hub2]) - len(placements_dict[hub2])) < 1:
        car2 = random.choice(placements_dict[hub2]) # choose a car to move
        filt_dict = dict(filter(lambda pair : int(limit_dict[pair[0]]) > len(pair[1]),
                                placements_dict.items())) # look for hubs with space available
        filt_dict = dict(filter(lambda pair : car2 in in_dict[pair[0]],
                                filt_dict.items())) # only look at hubs that can hold the car
        hub3 = random.choice(list(filt_dict))
        print(f'It seems that the {hub2} is out of room, so we need you to move the {car2} to the {hub3} first.')
        placements_dict[hub2].remove(car2)
        placements_dict[hub3] = placements_dict[hub3] + [car2]
    placements_dict[hub1].remove(car1)
    placements_dict[hub2] = placements_dict[hub2] + [car1]
    return placements_dict

def calc_points(points, streak):
    if streak % 10 == 0:
        points = points + 2
        if streak % 100 == 0:
            points = points + 20
            if streak % 1000 == 0:
                points = points + 200
    points = points + 1
    return points

def start_menu(hub_dict, current_placements, limit_dict):
    command = ''
    missions = 0
    points = 0
    streak = 0
    while command != 'abort':
        command = ''
        plural = '' if missions == 1 else 's'
        print(f'You have completed {missions} mission{plural}, and your current streak is {streak}.')
        print(f'Your points: {points}')
        print(f'Your cars are located in the following hubs:\n')
        print_placements(current_placements)
        print('Current mission:')
        current_placements = generate_operation(hub_dict, current_placements, limit_dict)
        while command != 'done' and command != 'skip' and command != 'abort':
            command = input('Get back to us when you are done (done/abort): ')
            streak = streak + 1 if command == 'done' else 0 if command == 'skip' else streak
            missions = missions + 1 if command == 'done' else missions
            points = calc_points(points, streak) if command == 'done' else points
            print(current_placements)
#             current_placements = current_placements if command == 'done' else current_placements
            print(current_placements)
        print()
    print('See you next time!')

### Main:
# Load layout information about hubs and cars:
hub_dict, limit_dict = parse_input('./operations_input.txt')

# Generate starting placements of cars:
car_placements = generate_placements(hub_dict, limit_dict)

if car_placements == "Too Many Cars":
    print(f'### Error ###\nYour hubs can not hold all of your cars. Add more hubs or reduce the number of cars in your input file.')
else:
    # Start missions:
    start_menu(hub_dict, car_placements, limit_dict)
