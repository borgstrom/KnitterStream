from PIL import Image, ImageDraw
import os
import logging
logger = logging.getLogger(__name__)


class E6000Pattern(object):
    """
    This class works with PIL images and turns them into the proper
    structure to be feed into the protocol class
    """

    def __init__(self, dir):
        self.dir = dir

    def process(self):
        """
        Process walks our directory looking for new files. When it
        finds them it runs them through process_file.

        It returns a list of the results from process_file
        """
        # make sure our "PROCESSED" directory exists
        processed_dir = os.path.join(self.dir, "PROCESSED")
        if not os.path.isdir(processed_dir):
            os.mkdir(processed_dir)

        # process
        for dirpath, dirnames, filenames in os.walk(self.dir):
            for filename in filenames:
                logger.info("Processing new file: %s" % filename)
                src_file = os.path.join(dirpath, filename)
                file_data = self.process_file(src_file)

                logger.info(" `-> Processed! Moving to processed dir...")
                os.rename(src_file, os.path.join(processed_dir, filename))

                return file_data

    def process_file(self, file):
        # open our image
        image = Image.open(file)

        # rotate it so that we can knit in order
        image = image.rotate(180)

        # get our pixel data
        data = []
        for pixel in image.getdata():
            # the order of colours on the knitting machine are:
            # 1 = colour
            # 2 = white
            # 3 = black
            if pixel == (0, 0, 0):
                data.append("3")
            elif pixel == (255, 255, 255):
                data.append("2")
            else:
                data.append("1")

        # return colours, columns (width), rows (height), [data]
        return (3,) + image.size + (data,)
