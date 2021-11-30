####
# Nick Bild
# November 2021
# Schematic-o-matic
# Automatically generate KiCad schematic from a populated breadboard.
# https://github.com/nickbild/schematic-o-matic
####


def get_components():
    # Ask user for component locations.
    components = []
    id = 0
    while True:
        component = input("Enter name of component: ")
        if component != "":
            pin1 = input("Enter column of pin 1: ")
            components.append([component.upper(), pin1, id])
            id += 1
        else:
            break

    return components


def map_pins_to_breadboard(components):
    bb_top = {}
    bb_bottom = {}

    # Determine locations of component pins on breadboard.
    for component in components:
        ic = component[0]
        pin1 = component[1]
        id = component[2]

        begin = False
        pin_cnt = 0
        for line in open("kicad_symbols/{0}.lib".format(ic), "r"):
            line = line.strip()

            if line == "ENDDRAW":
                begin = False

            if begin:
                if line.startswith("X "):
                    pin_cnt += 1

            if line == "DRAW":
                begin = True
        
        # Map component pins on bottom rows.
        pin_num = 1
        for i in range(int(pin1), int(pin1) - int(pin_cnt / 2), -1):
            if i not in bb_bottom:
                bb_bottom[i] = [id, pin_num]
            else:
                bb_bottom[i] = bb_bottom[i].append([id, pin_num])
            pin_num += 1

        # Map component pins on top rows.
        for i in range(int(pin1) - int(pin_cnt / 2) + 1, int(pin1) + 1, 1):
            if i not in bb_top:
                bb_top[i] = [id, pin_num]
            else:
                bb_top[i] = bb_top[i].append([id, pin_num])
            pin_num += 1

    return bb_top, bb_bottom


def retrieve_connections():
    conn_top = {}
    conn_bottom = {}

    # connections.scan file format:
    # 
    # TOP               # Header indicates following connections are initiated from top rows.
    # 30:P;             # column number : CSV of connecting columns on top rows ; CSV of connecting columns on bottom rows
    # 29:18;            # ...
    # BOTTOM            # Header indicates following connections are initiated from bottom rows.
    # 30:;              # ...
    
    top = False
    for line in open("connections.scan", "r"):
        line = line.strip()

        if line == "TOP":
            top = True
            continue
        elif line == "BOTTOM":
            top = False
            continue

        col = line.split(":")[0]
        top_row = line.split(":")[1].split(";")[0]
        bottom_row = line.split(":")[1].split(";")[1]
        
        if top:    
            conn_top[col] = [top_row.split(","), bottom_row.split(",")]
        else:
            conn_bottom[col] = [top_row.split(","), bottom_row.split(",")]

    return conn_top, conn_bottom


def add_components_to_schematic(components):
    x = 2000 
    y = 2000
    component_positions = {}

    sch = open("auto_schematic.sch", "w")
    
    # Header info.
    sch.write("""EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A2 23386 16535
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
""")

    # Add components.
    for component in components:
        ic = component[0]
        id = component[2]
        for line in open("component_definitions/{0}.def".format(ic), "r"):
            line = line.strip()
            if line.startswith("P "):
                sch.write("P {0} {1}\n".format(x, y))
                component_positions[id] = [x, y, ic]
                x += 6000
                if x > 50000:
                    x = 0
                    y += 6000
            else:
                sch.write("{0}\n".format(line))
    
    sch.close()

    return component_positions


def draw_wires(component_positions, bb_top, bb_bottom, conn_top, conn_bottom):
    sch = open("auto_schematic.sch", "a")

    # bb_top    {21: [0, 11], 22: [0, 12], 23: [0, 13], 24: [0, 14], 25: [0, 15], 26: [0, 16], 27: [0, 17], 28: [0, 18], 29: [0, 19], 30: [0, 20], 13: [1, 8], 14: [1, 9], 15: [1, 10], 16: [1, 11], 17: [1, 12], 18: [1, 13], 19: [1, 14]}
    # conn_top  {'30': [['P'], ['']], '29': [['18'], ['']], '28': [['P'], ['']], '27': [['P'], ['']], '26': [['G'], ['']], '25': [['G'], ['']], '24': [['P'], ['']], '23': [['P'], ['']], '22': [['G'], ['']], '21': [['G'], ['']], '20': [[''], ['']], '19': [['P'], ['']], '18': [['29'], ['']], '17': [['G'], ['']], '16': [['15'], ['']], '15': [['16'], ['']], '14': [['G'], ['']], '13': [[''], ['']], '12': [[''], ['']], '11': [[''], ['']], '10': [[''], ['']], '9': [[''], ['']], '8': [[''], ['']], '7': [[''], ['']], '6': [[''], ['']], '5': [[''], ['']], '4': [[''], ['']], '3': [[''], ['']], '2': [[''], ['']], '1': [[''], ['']]}

    # Top rows.
    for col in conn_top:
        if int(col) not in bb_top:
            continue

        # Start pin.
        id_start = bb_top[int(col)][0]
        pin_start = bb_top[int(col)][1]
        # End pin.
        for top_col in conn_top[col][0]:
            if top_col == "P" or top_col == "G":
                id_end = top_col
                pin_end = top_col
            elif top_col == "":
                continue
            else:
                id_end = bb_top[int(top_col)][0]
                pin_end = bb_top[int(top_col)][1]
            draw_single_wire(pin_start, pin_end, id_start, id_end, sch, component_positions)
        
        for bot_col in conn_top[col][1]:
            if bot_col == "P" or bot_col == "G":
                id_end = bot_col
                pin_end = bot_col
            elif bot_col == "":
                continue
            else:
                id_end = bb_bottom[int(bot_col)][0]
                pin_end = bb_bottom[int(bot_col)][1]
            draw_single_wire(pin_start, pin_end, id_start, id_end, sch, component_positions)

    # Bottom rows.
    for col in conn_bottom:
        if int(col) not in bb_bottom:
            continue

        # Start pin.
        id_start = bb_bottom[int(col)][0]
        pin_start = bb_bottom[int(col)][1]
        # End pin.
        for top_col in conn_bottom[col][0]:
            if top_col == "P" or top_col == "G":
                id_end = top_col
                pin_end = top_col
            elif top_col == "":
                continue
            else:
                id_end = bb_top[int(top_col)][0]
                pin_end = bb_top[int(top_col)][1]
            draw_single_wire(pin_start, pin_end, id_start, id_end, sch, component_positions)
        
        for bot_col in conn_bottom[col][1]:
            if bot_col == "P" or bot_col == "G":
                id_end = bot_col
                pin_end = bot_col
            elif bot_col == "":
                continue
            else:
                id_end = bb_bottom[int(bot_col)][0]
                pin_end = bb_bottom[int(bot_col)][1]
            draw_single_wire(pin_start, pin_end, id_start, id_end, sch, component_positions)
    
    sch.write("$EndSCHEMATC")

    sch.close()

    return


def draw_single_wire(pin_start, pin_end, id_start, id_end, sch, component_positions):
    if pin_end == "P" or pin_end == "G":
        print("{}:{} to {}".format(id_start, pin_start, pin_end))
    else:
        print("{}:{} to {}:{}".format(id_start, pin_start, id_end, pin_end))
        
        x_offset, y_offset = get_pin_offset(component_positions[id_start][2], pin_start)
        # print(component_positions[id_start][0])
        # print(component_positions[id_start][1])
        # print(x_offset)
        # print(y_offset)

        start_x = component_positions[id_start][0] + x_offset
        start_y = component_positions[id_start][1] + y_offset

        x_offset, y_offset = get_pin_offset(component_positions[id_end][2], pin_end)
        # print(component_positions[id_end][0])
        # print(component_positions[id_end][1])
        # print(x_offset)
        # print(y_offset)

        end_x = component_positions[id_end][0] + x_offset
        end_y = component_positions[id_end][1] + y_offset

        sch.write("""Wire Wire Line
	{0}  {1} {2}  {3}\n""".format(start_x, start_y, end_x, end_y))

    return


def get_pin_offset(component_name, pin_number):
    x_offset = 0
    y_offset = 0

    begin = False
    for line in open("kicad_symbols/{0}.lib".format(component_name), "r"):
        line = line.strip()

        if line == "ENDDRAW":
            begin = False

        if begin:
            if line.startswith("X "):
                pin_num = line.split(" ")[2]
                if int(pin_num) == int(pin_number):
                    x_offset = int(line.split(" ")[3])
                    y_offset  = -1 * int(line.split(" ")[4])

        if line == "DRAW":
            begin = True

    return x_offset, y_offset


def main():
    components = get_components()
    bb_top, bb_bottom = map_pins_to_breadboard(components)
    conn_top, conn_bottom = retrieve_connections()
    component_positions = add_components_to_schematic(components)
    draw_wires(component_positions, bb_top, bb_bottom, conn_top, conn_bottom)


if __name__ == "__main__":
    main()
