KnitterStream - The code
========================

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
the serial port using the [DesignaKnit][1] serial cable. It also uses
the protocol of the Arduino portion to trigger the actions in the
order that we need them to happen.

It watches a directory for new PNG files, sorted by filename (so use
timestamps to guarantee processing order), and for each file it finds
it will quantize the image to our standard 3-colour pallete (black,
red & white), rotates the image 180 degrees, packs the data into the
format wanted by the E6000 and finally writes it to the E6000.


[1]: http://www.softbyte.co.uk/dk7.htm
