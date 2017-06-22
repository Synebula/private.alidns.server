#!/usr/bin/python
#-*- coding:utf-8 -*-
'''logger'''

from __future__ import print_function
import time

def log(*msg):
    '''print the msg'''
    print('[%s] ' % time.ctime(), end='')
    for item in msg[:-1]:
        print(item, end=', ')
    print(msg[-1])
