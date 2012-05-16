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

    # forever...
    state = "ready"
    pattern_data = None
    try:
        while loop is True:
            if state == "ready":
                logger.info("Ready to load a new pattern!")

                pattern_data = pattern.process()
                if not pattern_data:
                    logger.error("No pattern data available :'(")
                    time.sleep(5)
                    continue

                logger.info("Loaded a new pattern! colours=%d columns=%d rows=%d" % pattern_data[:3])

                arduino.send(">")

                raw_input("Flip the switch to program mode, press enter when ready... ")
                state = "program1"

            if state == "program1":
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

                raw_input("Flip the switch to knit mode, press enter when ready... ")
                state = "program2"

            if state == "program2":
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

                raw_input("Press the MOTOR ONE WAY button, then the MOTOR GO button")

                arduino.send([
                    "E",
                    "E"
                    ])

                raw_input("Press the MOTOR ONE WAY button, then the MOTOR GO button")

                arduino.send([
                    "E",
                    "E",
                    "E",
                    "E",
                    "E",
                    "E",
                    "E"
                    ])

                raw_input("Press the MOTOR GO button")

                state = "knitting"

            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt, exiting...")

    e6000.close()
