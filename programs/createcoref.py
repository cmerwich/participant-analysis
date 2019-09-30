import getopt
import os, sys
from sys import argv, exit, stderr
  
def Usage():
    stderr.write('usage: createcoref book_name first_chapter [last_chapter]\n')
    exit(1)
    
def CreateCoref(book_name, first_chapter, last_chapter):
    print(book_name, first_chapter, last_chapter)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'v', [])
    except getopt.GetoptError:
        Usage()
    print(len(args), len(argv))
    if len(args) == 2:
        last_chapter = int(args[1])
    elif len(args) == 3:
        last_chapter = int(args[2])
    else:
        Usage()   
    
    first_chapter = int(args[1])
    book_name = args[0]
    
    CreateCoref(book_name, first_chapter, last_chapter)

if __name__ == "__main__":
    main(argv[1:])