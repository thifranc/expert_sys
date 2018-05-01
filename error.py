#!/usr/bin/python3

class Error:

  def __init__(self, error_type, error_msg = ''):
    print('Error type: ', error_type, ' has been thrown with msg : ', error_msg)
    exit(1)
