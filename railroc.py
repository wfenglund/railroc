# input: a text-file containing possible hubs with possible cars with possible states [cargo/people 0/1/2] (0 == empty, 1 == full, 2 == either)
# example row:
# hub1;car1|cargo 0,car2|people 1

import random

def generate_placements(in_dict):
    hub_dict = {k: [] for k in list(in_dict)}
    key_list = [list(i[1]) for i in in_dict.items()]
    car_set = set([i for j in key_list for i in j])
    car_list = list(car_set)
    for car in car_list:
        filt_dict = dict(filter(lambda pair : car in pair[1], in_dict.items()))
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
    with open(input_file) as file:
        for line in file:
            hub_name, hub_info = line.split(';')
            car_dict = {}
            for car_entry in hub_info.strip().split(','):
                car = car_entry.split('|')
                car_dict[car[0]] = car[1]
            if hub_name in list(hub_dict): # if this is not the first entry of this hub
                hub_dict[hub_name] = merge_dicts(car_dict, hub_dict[hub_name])
            else:
                hub_dict[hub_name] = car_dict
    return hub_dict

def generate_operation(in_dict, placements_dict):
    filt_dict = dict(filter(lambda pair : len(placements_dict[pair[0]]) > 0, in_dict.items()))
    hub1, car_dict1 = random.choice(list(filt_dict.items()))
    car1 = random.choice(placements_dict[hub1])
    meta1 = car_dict1[car1]
    type1, nmbr = meta1.split() # type1 is not used
    state1 = 'empty' if nmbr == '0' else 'full' if nmbr == '1' else random.choice(['empty', 'full'])
    filt_dict = dict(filter(lambda pair : car1 in pair[1], in_dict.items()))
    filt_dict.pop(hub1)
    hub2, car_dict2 = random.choice(list(filt_dict.items())) # car_dict2 is not used
    print(f'We need you to bring the {state1} {car1} from the {hub1} to the {hub2}.')
    placements_dict[hub1].remove(car1)
    placements_dict[hub2] = placements_dict[hub2] + [car1]
    return placements_dict

def start_menu(layout_info, car_placements):
    points = 0
    command = ''
    while command != 'abort':
        command = ''
        plural = '' if points == 1 else 's'
        print(f'You have completed {points} mission{plural}. Your cars are located in the following hubs:\n')
        print_placements(car_placements)
        print('Current mission:')
        car_placements = generate_operation(layout_info, car_placements)
        while command != 'done' and command != 'abort':
            command = input('Get back to us when you are done (done/abort): ')
            points = points + 1 if command == 'done' else points
        print()
    print('See you next time!')

### Main:
# Load layout information about hubs and cars:
layout_info = parse_input('./operations_input.txt')

# Generate starting placements of cars:
car_placements = generate_placements(layout_info)

# Start missions:
start_menu(layout_info, car_placements)
