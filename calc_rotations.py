import math
import sys



def advance_film(distance, diameter, thickness, counter):
    """ Advances film with finer updates per turn. """
    total_turns = 0
    total_degrees = 0
    while distance > 0:
        step_turns = step_size  # Turns per step
        
        # Calc step distance with circumrence at start of step, less precise
        #circumference = math.pi * diameter
        # step_distance = circumference * step_size

        # Calc step distance with circumfrence at middle of step, more precise
        next_diameter = diameter - 2 * step_size * thickness
        mid_diameter = (diameter + next_diameter) / 2
        step_distance = math.pi * mid_diameter * step_size

        if distance - step_distance < 0:
            step_turns *= (distance / step_distance)  # Adjust last step
            step_distance = distance

        distance -= step_distance
        total_turns += step_turns
        total_degrees += step_turns * 360  # Convert turns to degrees
        diameter -= 2 * step_turns * thickness  # Update diameter with thickness decrease
        counter += 1
        if (counter % steps_percent ) == 0:
            percent = counter / steps_percent
            filled_length = int(counter / steps_percent)
            bar = '#' * filled_length + '-' * (100-filled_length)
            sys.stdout.write(f"\r {bar} {round(percent,0)}%")
            sys.stdout.flush()
            

    return total_turns, total_degrees, diameter, counter

print("Enter 1 for 6x6, 2 for 6x12, 3 for 6x3: ")

while True:
    try:
        selection = int(input())
        break
    except ValueError:
        print("Not a number")

initial_diameter = 21.6  # mm
film_thickness_paper = 0.1  # mm
film_thickness_total = 0.22  # mm
update_steps = 10000.0 
relative_degrees = 370
counter = 0

if selection == 1:
    initial_advance_paper = 268  # mm war 337.5
    initial_advance_film = 66 # mm
    frame_distance = 64  # mm
    num_frames = 12
    total_steps = 178259228
    steps_percent = 1782592
    
elif selection == 2:
    initial_advance_paper = 296  # mm war 337.5
    initial_advance_film = 100 # mm
    frame_distance = 128  # mm
    num_frames = 6
    total_steps = 176887976
    steps_percent = 1768879
elif selection == 3:
    initial_advance_paper = 268  # mm war 337.5
    initial_advance_film = 52 # mm
    frame_distance = 33  # mm
    num_frames = 24
    total_steps = 187244373
    steps_percent = 1872443 


   
else:
    sys.exit("Number not 1 or 2")

diameter = initial_diameter
turns_list = []
step_size = 1.0 / update_steps  # Fractional step updates


# First film advance first part only paper, then to frame 1 with film
advance_1, degrees_1, diameter, counter = advance_film(initial_advance_paper, diameter, film_thickness_paper, counter)

advance_2, degrees_2, diameter, counter = advance_film(initial_advance_film , diameter, film_thickness_total, counter)

total_advance = advance_1 + advance_2
total_degrees = degrees_1 + degrees_2
turns_list.append((1, total_advance, total_degrees, diameter))

# Advances for each frame (64mm per frame)
for i in range(2, num_frames + 1):
    turns, degrees, diameter, counter = advance_film(frame_distance, diameter, film_thickness_total, counter)
    turns_list.append((i, turns, degrees, diameter))


print("\n  Frame  | Relative Degrees |  Turns   | Total Degrees |")
print("---------------------------------------------------------")
for frame, turns, degrees, diameter in turns_list:
    relative_deg = degrees % 360  # Normalize within 0–360
    print(f"|   {frame:2d}   |     {relative_deg:7.2f}     | {turns:7.4f} |   {degrees:8.2f}   |")

print(counter)
