KnitterStream - The code
========================

The [KnitterStream][ks] is an electronics based art project that is being
put together for the [C2-MTL][c2] conference. It consists of some hardware
mods to a [Passap E6000][e6000], some ingenuity in tricking the E6000 into
doing things it was not meant to do as well as some Python & Processing
code to handle the generation of our patterns. Check out the [KnitterStream][ks]
website for more information.

The KnitterStream is a collaboration between [Sid-Lee][sl], [FatBox][fb] and
[Lunch][lu].

Arudino Code
------------
The Arudino portion of the project is a mod to the E6000 control panel
and motor control buttons to allow button presses to be triggered via
the Python application (below).

It exposes a very simple protocol that signals which button should be
triggered by receiving a single byte over the serial port of the
Arduino itself. See the code for the current map of button codes.


Python Code
-----------
The Python portion is a daemon which runs and controls the E6000 via
the serial port using the [DesignaKnit][dk] serial cable. It also uses
the protocol of the Arduino portion to trigger the actions in the
order that we need them to happen.

It watches a directory for new PNG files, sorted by filename (so use
timestamps to guarantee processing order), and for each file it finds
it will quantize the image to our standard 3-colour pallete (black,
red & white), rotates the image 180 degrees, pack the data into the
format wanted by the E6000 and finally writes it to the E6000.

The PNG files should be a 1:1 mapping of pixel to stitch. If you want
a pattern with 90 columns & 120 rows then the PNG should be 90x120 as
well.


[ks]: http://www.knitterstream.com
[dk]: http://www.softbyte.co.uk/dk7.htm
[c2]: http://c2mtl.com/
[e6000]: http://www.knittingmachinemuseum.com/Passap_E6000.php
[sl]: http://www.sidlee.com/
[fb]: http://fatbox.ca/
[lu]: http://thelunchsite.com/
