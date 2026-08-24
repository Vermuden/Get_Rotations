import math
import sys
import csv



def advance_film(distance, diameter, thickness, counter):
    """ Advances film with finer updates per turn. """
    total_turns = 0
    total_degrees = 0
    while distance > 0:
        step_turns = step_size  # Turns per step
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
            bar = '#' * filled_length  + '.' * (100-filled_length)
            sys.stdout.write(f"\r {bar} {round(percent,0)}%")
            sys.stdout.flush()
            

    return total_turns, total_degrees, diameter, counter


def export_relative_degrees_csv(turns_list, filename="relative_degrees.csv"):
    """Exports relative degrees for each frame to a CSV file to import as user parameter in fusion 360.
    
    Format: <name>, <unit>, <expression>, <value>, <comment>, <favourite>
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "unit", "expression","value", "comment", "favourite"])
        for frame, turns, degrees, diameter in turns_list:
            relative_deg = degrees % 360
            writer.writerow([f"f{frame}", "°", f"{relative_deg:.2f}","", "", ""])
    print(f"\nRelative degrees exported to '{filename}'")


###


print("Enter 1 for 6x6, 2 for 6x12, 3 for 6x3, 4 for 6x12 (Gideon), 5 for 6x6 Nona Wide: ")

while True:
    try:
        selection = int(input())
        break
    except ValueError:
        print("Not a number")

initial_diameter = 21.8  # mm
film_thickness_paper = 0.11  # mm
film_thickness_total = 0.25  # mm
update_steps = 1000000.0 
relative_degrees = 370
counter = 0

if selection == 1: # 6x6
    initial_advance_paper = 268  # mm war 337.5
    initial_advance_film = 66 # mm
    frame_distance = 64  # mm
    num_frames = 12
    total_steps = 178259228
    steps_percent = 1782592
elif selection == 2: # 6x12 v0.1
    initial_advance_paper = 296  # mm war 337.5
    initial_advance_film = 100 # mm
    frame_distance = 128  # mm
    num_frames = 6
    total_steps = 176887976
    steps_percent = 1768879
elif selection == 3: # 6x3
    initial_advance_paper = 188  # mm war 337.5
    initial_advance_film = 30 + 32 # mm
    frame_distance = 33.5  # mm
    num_frames = 24
    total_steps = 169815297
    steps_percent = 1698152 
elif selection == 4: # 612 Gideon
    initial_advance_paper = 188  # mm war 337.5
    initial_advance_film = 35 + 128 # mm
    frame_distance = 129  # mm
    num_frames = 6
    total_steps = 168734218
    steps_percent = 1687342
elif selection == 5: #Nona 2 (Wide)
    initial_advance_paper = 188 # mm war 337.5
    initial_advance_film = 35 + 60 # mm
    frame_distance = 66  # mm
    num_frames = 12
    total_steps = 173491191
    steps_percent = 1734912
else:
    sys.exit("Enter a number between 1 and 4.")

diameter = initial_diameter
turns_list = [] # frame number | turns to next Frame | Degrees to next Frame | Diameter | Total Turns from Zero | Realtive Degrees from Zero
step_size = 1.0 / update_steps  # Fractional step updates


# First film advance first part only paper, then to frame 1 with film
turns_1, degrees_1, diameter, counter = advance_film(initial_advance_paper, diameter, film_thickness_paper, counter)

turns_2, degrees_2, diameter, counter = advance_film(initial_advance_film , diameter, film_thickness_total, counter)

total_turns = turns_1 + turns_2
total_degrees = degrees_1 + degrees_2
relative_zero = total_degrees % 360
turns_list.append([1, total_turns, total_degrees, diameter, total_degrees, relative_zero])

# Advances for each frame (64mm per frame)
for i in range(2, num_frames + 1):
    turns, degrees, diameter, counter = advance_film(frame_distance, diameter, film_thickness_total, counter)
    total_degrees = total_degrees + degrees
    relative_zero = total_degrees % 360
    turns_list.append([i, turns, degrees, diameter, total_degrees, relative_zero])

sorted_list = sorted(turns_list, key=lambda turns_list: turns_list[5])

#print("| Frame | Delta to frame in line above |")
#for frame, turns, degrees, diameter,total_degrees, relative_zero in sorted_list:
#      print(f"| {frame:2d} | {relative_zero:8.2f} |")

sorted_list.insert(0, [0, 0, 0, initial_diameter, 0, 0,0])
# Calc Delta to Frame relative Frame before relative; not number but in order of appearence on a circle
for i in range(1, num_frames+1):
    delta = sorted_list[i][5] - sorted_list[i-1][5]
    sorted_list[i].append(delta)

print("\n| Frame  | Relative Degrees |  Turns   | Total Degrees next Frame | Total Degrees from Zero |")
print("-----------------------------------------------------------------------------------------------")
for frame, turns, degrees, diameter, total_degrees, relative_zero, delta in turns_list:
    relative_deg = degrees % 360  # Normalize within 0–360
    print(f"|   {frame:2d}   |     {relative_deg:7.2f}     | {turns:7.4f} |   {degrees:8.2f}   |      {total_degrees:8.2f} |     {relative_zero:8.2f} |\n---------------------------------------------------------------------")

print("\n\n--------------------------------------------------------------------\n\n")

print("| Frame | Delta to frame in line above |")
for frame, turns, degrees, diameter,total_degrees, relative_zero, delta in sorted_list:
      print(f"| {frame:2d} | {delta:8.2f} |")

print(counter)
export_relative_degrees_csv(turns_list)
