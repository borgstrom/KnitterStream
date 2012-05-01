import serial

import logging
logger = logging.getLogger(__name__)
 
class E6000Serial(object):
    """
    This class encapsulates the functionality for interfacing with
    a Passap E6000 via its serial port.

    The E6000 is a VERY simple machine. Too simple infact. Getting
    the protocol right required me to think as simply as possible.

    For input (what it sends to us) there is only one thing that it
    sends over the serial port; a single null byte each time the row
    counter is triggered.
    
    For output we need to send a plain text string that is described
    in the HEADER_FORMAT & DATA_FORMAT templates. The string should
    be constructed entirely and then written to the serial device in
    one shot.
    """

    # These are the templates used for constructing the data we will
    # send to the E6000.
    # colours: the number of colours in this pattern
    # columns: the number of columns in this pattern
    # rows: the number of rows in this pattern
    #
    # The data is a series of "0", "1", "2" or "3" characters (yes
    # ascii strings, weird) to represent which colour to make the
    # foreground. There is no RLE or anything, just straight data.
    HEADER_FORMAT = "%(colours)s %(columns)3s %(rows)3s"
    DATA_FORMAT = "%(header)s %(data)s\x03"

    def __init__(self, port):
        logger.info("Initializing E6000 serial interface...")
        self.serial = serial.Serial(port, 1200,
                parity=serial.PARITY_EVEN)
        logger.info(" `-> Initialized!")

    def close(self):
        if self.serial:
            logger.info("Closing E6000 serial interface...")
            self.serial.close()
            logger.info(" `-> Closed!")

    def send(self, colours, columns, rows, data):
        if self.serial:
            # build our header data
            header = E6000Serial.HEADER_FORMAT % {
                    'colours': colours,
                    'columns': columns,
                    'rows': rows
                    }

            # and the full payload
            payload = "%(header)s %(data)s\x03" % {
                    'header': header,
                    'data': ''.join([stitch for stitch in data]),
                    }

            # write it
            self.serial.write(payload)
