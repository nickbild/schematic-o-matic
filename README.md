# Schematic-o-matic

Schematic-o-matic automatically draws a KiCad schematic for a circuit prototyped on a breadboard.

![](https://github.com/nickbild/schematic-o-matic/raw/main/media/breadboard_w_arduino_title_sm.jpg)

## How It Works

The first step in the process is to use a specially instrumented breadboard to build your circuit on.  Each continuous condictive region on the breadboard has a wire soldered to it on the underside of the breadboard.  This allows for a methodical test for electrical continuity between each region, which was accomplished by using an Arduino Due [code here](https://github.com/nickbild/schematic-o-matic/tree/main/connection_tester).

Because certain components (e.g. ICs) can cause false positives for connections between regions due to internal conductances, they must be removed from the board before running the Arduino code.  The output of the code is a map of the electrical connections between regions (i.e. wire placements).

This connections map is then processed by a [Python script](https://github.com/nickbild/schematic-o-matic/blob/main/draw_schematic.py).  It begins by asking for the locations of components on the boards with a minimum of information, e.g.:

```
Enter name of component: sn74ls682n
Enter column of pin 1: 30
Enter name of component: sn74hc32n
Enter column of pin 1: 19
Enter name of component: 
```

For clarity, the above data would correspond to this simple circuit:

![](https://github.com/nickbild/schematic-o-matic/raw/main/media/breadboard_populated_annotated_sm.jpg)

To determine the location of all component pins on the breadboard, the script parses the associated KiCad library file.  The components are added to a KiCad schematic (`EESchema Schematic File Version 4` format), after which the wires are then added, according to the connections information collected through continuity testing, with the help again of KiCad library files to determine the locations of all pins to place wires in the correct locations.

The end result of running Schematic-o-matic on the above circuit is this KiCad schematic:

TODO: insert schematic here

## Media

Schematic-o-matic instrumented breadboard and Arduino Due:
![](https://github.com/nickbild/schematic-o-matic/raw/main/media/breadboard_w_arduino_sm.jpg)

A simple circuit for testing:
![](https://github.com/nickbild/schematic-o-matic/raw/main/media/breadboard_populated_sm.jpg)

Breadboard with bottom removed (getting all the sticky bits off is impossible):
![](https://github.com/nickbild/schematic-o-matic/raw/main/media/breadboard_bottom_sm.jpg)

Breadboard circuit with components removed:
![](https://github.com/nickbild/schematic-o-matic/raw/main/media/breadboard_empty_sm.jpg)

## Bill of Materials

- 1 x Arduino Due (or Mega, or similar)
- 1 x breadboard
- Wires

## About the Author

[Nick A. Bild, MS](https://nickbild79.firebaseapp.com/#!/)
