from PIL import Image, ImageDraw

PALETTE = [
        0,   0,   0,   # black
        255, 0,   0,   # red
        255, 255, 255, # white
        ] + [0, ] * 253 * 3

class E6000Pattern(object):
    """
    This class works with PIL images and turns them into the proper
    structure to be feed into the protocol class
    """

    def __init__(self, dir):
        self.dir = dir

    def process(self):
        for dirname, dirnames, filenames in os.walk(self.dir):
            for filename in filenames:
                logger.info("Processing new file: %s" % filename)

    def process_file(self, file):
        # a palette image to use for quantization
        pimage = Image.new("P", (1, 1), 0)
        pimage.putpalette(PALETTE)

        # open our image
        image = Image.open(file)
        
        # quantize it
        image = image.quantize(palette=pimage)

        # rotate it so that we can knit in order
        image = image.rotate(180)

        # get our pixel data
        data = [pixel for pixel in image.getdata()]

        # return colours, columns (width), rows (height), [data]
        return (3,) + image.size + (data,)
