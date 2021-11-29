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

    sch = open("auto_schematic_TEST.sch", "w")
    
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
                component_positions[id] = [x, y]
                x += 6000
                if x > 50000:
                    x = 0
                    y += 6000
            else:
                sch.write("{0}\n".format(line))
    
    sch.close()

    return component_positions


def draw_wires(components, component_positions):
    sch = open("auto_schematic_TEST.sch", "a")

    sch.write("$EndSCHEMATC")

    sch.close()

    return


def main():
    components = get_components()
    bb_top, bb_bottom = map_pins_to_breadboard(components)
    conn_top, conn_bottom = retrieve_connections()
    component_positions = add_components_to_schematic(components)
    draw_wires(components, component_positions)


if __name__ == "__main__":
    main()
