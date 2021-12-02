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

To determine the location of all component pins on the breadboard, the script parses the associated KiCad library file.  The components are added to a KiCad schematic (`EESchema Schematic File Version 4` format), after which the wires are then added, according to the connections information collected through continuity testing, with the help again of KiCad library files to determine the locations of all pins to place wires in the correct locations.  The plain text, open formats used by KiCad made this integration possible.

The end result of running Schematic-o-matic on the above circuit is this KiCad schematic:

![](https://github.com/nickbild/schematic-o-matic/raw/main/media/schematic.png)

## Limitations

For continuity testing to be accurate, certain components need to be removed before testing.  While this is inconvenient, I believe that the benefit of having all wires mapped out so quickly (and guaranteed to be error free!) is still a big win.  I have built a number of very complex breadboard circuits (see [Vectron VGA](https://github.com/nickbild/vectron_vga), for example) that took days to trace all the wires for the schematic (then cross my fingers hoping I didn't make even one mistake).  A tool like this would have saved me many, many hours of unpleasant work.

The schematics will be accurate, but may not be pretty.  I have implemented wires as straight lines between connection points.  I think they could be made to run parallel to one another, rather than randomly overlap, it would just take a more complex algorithm with some awareness of other wiring.

For this prototype, I have focused on ICs.  Adding other components would be possible in principle using the same basic approach of asking the user for key points, and collecting the bulk of the information from KiCad library files.  Again, it's just a matter of putting more time into it.

The protoype design uses a lot of pins (one for each conductive region on the breadboard) for continuity testing to keep things simple.  For larger designs, that's not reasonable.  Some type of multiplexing would need to be implemented.

While not necessarily a limitaiton, the current text-based interface is a bit crude.  A graphic interface that allows a library of components to be drag-and-dropped onto a virtual breadboard would make the process more intuitive, I believe.

## Media

Demonstration video: [YouTube](https://www.youtube.com/watch?v=L2e3amMnLaA)

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
