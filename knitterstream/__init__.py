from optparse import OptionParser

from knitterstream.protocol import E6000Serial, ArduinoSerial
from knitterstream.pattern import E6000Pattern

import logging
import signal
import time
import sys
import os

logger = logging.getLogger(__name__)
loop = True

def main():
    """
    Main entry point
    """
    usage = "usage: %prog -s e6000-serial -a arduino-serial -d watch/ [-t ~/.twitter-creds]"
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--e6000', dest='e6000', metavar='PORT',
            help='The serial port to communicate with the E6000 on, can be any valid pySerial name')
    parser.add_option('-a', '--arduino', dest='arduino', metavar='PORT',
            help='The serial port to communicate with the Arduino on, can be any valid pySerial name')
    parser.add_option('-d', '--dir', dest='dir',
            help='The directory to watch for new files')
    parser.add_option('-t', '--twitter', dest='twitter', metavar='FILE',
            help='Specify a file containing Twitter API credentials')
    parser.add_option('-l', '--log', dest='log', metavar='FILE',
            help='Log output to a file also')

    (options, args) = parser.parse_args()

    # setup logging
    formatter = logging.Formatter('%(asctime)s %(levelname)s\t%(message)s')
    logger.setLevel(logging.DEBUG)

    # log to stdout always
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # do we have a file
    if options.log:
        file_handler = logging.FileHandler(options.log)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not options.e6000:
        parser.error("You must specify a serial port for the E6000")

    if not options.arduino:
        parser.error("You must specify a serial port for the Arduino")

    if not options.dir:
        parser.error("You must specify a directory to watch")

    if not os.path.isdir(options.dir):
        parser.error("Invalid directory specified: %s" % options.dir)

    logger.info("KnitterStream - Starting up...")

    # initialize our protocol
    e6000 = E6000Serial(options.e6000)
    arduino = ArduinoSerial(options.arduino)

    # and our pattern
    pattern = E6000Pattern(options.dir)

    # install a TERM handler to toggle our loop variable
    def term_handler(signum, frame):
        global loop
        loop = False
        logger.info("Caught TERM signal, exiting...")
    signal.signal(signal.SIGTERM, term_handler)

    # set our baseline
    state = "ready"
    pattern_data = None
    row_count = 0
    expected_rows = 0

    # forever...
    try:
        while loop is True:
            """
            if state == "knitting":
                # while knitting we'll get null bytes for each pass
                # that the carriage makes a pass
                if e6000.read():
                    row_count += 1
                else:
                    continue

                # status update?
                if row_count % 10 == 0:
                    logger.info("%d rows to go..." % expected_rows - row_count)

                # when we reach 1 before our expected rows
                # then we need to sleep for 1 second and press the
                # one way button so it stops on the way back
                if row_count == (expected_rows - 1):
                    time.sleep(1)
                    arduino.send("O")

                    time.sleep(5)

                    # before we go back to ready state we need to
                    # first change the carriage direction and turn
                    # off the colour change option
                    arduino.send("C")
                    arduino.send("S")

                    # return to ready state
                    state = "ready"
            """

            if state == "ready":
                logger.info("Ready to load a new pattern!")

                pattern_data = pattern.process()
                if not pattern_data:
                    logger.error("No pattern data available :'(")
                    time.sleep(5)
                    continue

                logger.info("Loaded a new pattern! colours=%d columns=%d rows=%d" % pattern_data[:3])

                arduino.send(">")

                # toggle the switch
                arduino.send("T")
                time.sleep(5)

                # send the commands to prepare for pattern loading
                logger.info("Setting up the E6000 for programming...")
                arduino.send([
                    "E",
                    "E",
                    "3",
                    "E",
                    "N",
                    "B",
                    "0"
                    ])
                logger.info(" `-> Done!")

                # now send the pattern
                logger.info("Loading pattern to the E6000...")
                e6000.send(pattern_data[0], pattern_data[1], pattern_data[2], pattern_data[3])
                logger.info(" `-> Done!")

                # toggle the switch back
                arduino.send("T")
                time.sleep(5)

                # finish the programming
                arduino.send([
                    "N",
                    "1", "9", "8", "E",
                    "N",
                    "N",
                    "E",
                    "N",
                    "4", "5", "-", "E",
                    "4", "5", "E",
                    "N",
                    "E",
                    "A",
                    "E",
                    "E",
                    "E",
                    ])

                time.sleep(1)

                # press motor switch color, motor one way, then motor go
                arduino.send([
                    "C",
                    "O",
                    "G"
                    ])
                time.sleep(5)

                arduino.send([
                    "E",
                    "E"
                    ])

                # press motor one way, then motor go
                arduino.send([
                    "O",
                    "G"
                    ])
                time.sleep(5)

                arduino.send([
                    "E",
                    "E",
                    "E",
                    "E",
                    "E",
                    "E",
                    "E"
                    ])

                time.sleep(1)

                # set our new state
                #state = "knitting"

                # save the number of rows we're expected to knit for
                # this pattern, this is the number of rows from the
                # pattern data multiplied by the number of colours
                # and finally multiplied by 2 (since we get a row
                # count for each pass of the carriage)
                expected_rows = pattern_data[0] * pattern_data[2] * 2
                row_count = 0

                # GO!
                arduino.send([
                    "G"
                    ])

                raw_input("The pattern is now being knitted. Press the One-Way button when you reach %d row count, then press any key to process the next pattern" % ((expected_rows - 1),))

            # wait for a short amount of time
            time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt, exiting...")

    e6000.close()
    arduino.close()
