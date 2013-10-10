#! /usr/bin/env python

import os
import sys

BIN_DIR = os.path.abspath(os.path.dirname(__file__))
SLIDE_DIR = os.path.abspath(os.path.dirname(BIN_DIR))
IMAGE_DIR = os.path.abspath(os.path.join(SLIDE_DIR, 'images'))
BASE_DIR = os.path.abspath(os.path.dirname(SLIDE_DIR))
REDUX_DIR = os.path.abspath(os.path.join(BASE_DIR, 'response-redux'))
REDUX_RESULT_DIR = os.path.abspath(os.path.join(REDUX_DIR, 'results'))
VALIDATION_DIR = os.path.abspath(os.path.join(BASE_DIR, 'validation'))
VALIDATION_RESULT_DIR = os.path.abspath(os.path.join(VALIDATION_DIR, 'results'))

def main():
    sys.stdout.write("%s" % PROJECT_DIR)

if __name__ == '__main__':
    main()

