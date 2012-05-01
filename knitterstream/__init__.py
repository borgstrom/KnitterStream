from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('-t', '--twitter', dest='twitter',
            help='Specify a file containing Twitter API credentials')
    parser.add_option('-d', '--dir', dest='dir',
            help='The directory to watch for new files')

    (options, args) = parser.parse_args()
