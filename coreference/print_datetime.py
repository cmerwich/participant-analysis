from datetime import datetime
import getpass

def print_datetime():

    print('Notebook last updated by {} at {}'.format(getpass.getuser(), datetime.now().__str__()))
