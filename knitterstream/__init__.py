from optparse import OptionParser

from knitterstream.protocol import E6000Serial

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
    usage = "usage: %prog -s serial-port -d watch/ [-t ~/.twitter-creds]"
    parser = OptionParser(usage=usage)
    parser.add_option('-s', '--serial', dest='serial', metavar='PORT',
            help='The serial port to use, can be any valid pySerial name')
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

    if not options.serial:
        parser.error("You must specify a serial port")

    if not options.dir:
        parser.error("You must specify a directory to watch")

    if not os.path.isdir(options.dir):
        parser.error("Invalid directory specified: %s" % options.dir)

    logger.info("KnitterStream - Starting up...")

    # initialize our protocol
    serial = E6000Serial(options.serial)

    # install a TERM handler to toggle our loop variable
    def term_handler(signum, frame):
        global loop
        loop = False
        logger.info("Caught TERM signal, exiting...")
    signal.signal(signal.SIGTERM, term_handler)

    # forever...
    try:
        while loop is True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt, exiting...")

    serial.close()
