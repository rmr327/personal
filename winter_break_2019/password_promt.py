import argparse
import getpass


class Password:

    DEFAULT = 'Prompt if not specified'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass.getpass('W2W Password: ')
        self.value = value

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-u', '--username', help='Specify username', default=getpass.getuser())
parser.add_argument('-p', '--password', type=Password, help='Specify password', default=Password.DEFAULT)
args = parser.parse_args()
