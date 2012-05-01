from optparse import OptionParser

from knitterstream.protocol import E6000Serial

import time
import sys
import os

import logging
logger = logging.getLogger(__name__)

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

    serial = E6000Serial(options.serial)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt, exiting...")

    serial.close()
