KnitterStream - The code
========================

This is the Python application that drives the KnitterStream project.

It is essentially a server daemon that watches a directory for new png
files and then communicates with the Passap E6000 knitting machine.

The png's it finds are converted into the commands needed to knit them
at a 1:1 pixel to stitch mapping.
