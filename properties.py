#!/usr/bin/python
#-*- coding:utf-8 -*-
'''resolve properties file'''

import re
import os
import tempfile

def load_properties(file_name):
    '''load a new Properoties instanse, you can chage the properties file'''
    return Properties(file_name)

def load_properties_dict(file_name):
    '''load a properties dict, you can not chage the properties file'''
    return Properties(file_name).properties

class Properties(object):
    '''properties reslover'''

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception, ex:
            raise ex
        else:
            fopen.close()

    def has_key(self, key):
        '''valid there has this key'''
        return key in self.properties

    def get(self, key, default_value=''):
        '''get value of key'''
        if key in self.properties:
            return self.properties[key]
        return default_value

    def update(self, key, value):
        '''update value of key'''
        self.properties[key] = value
        self.replace_properties(key + '=.*', key + '=' + value, True)


    def replace_properties(self, old, new, append_on_not_exists=True):
        '''replace properties file'''
        tmpfile = tempfile.TemporaryFile()

        if os.path.exists(self.file_name):
            read_file = open(self.file_name, 'r')
            pattern = re.compile(r'' + old)
            found = None
            for line in read_file:
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(old, new, line)
                tmpfile.write(line)
            if not found and append_on_not_exists:
                tmpfile.write('\n' + new)
            read_file.close()
            tmpfile.seek(0)

            content = tmpfile.read()

            if os.path.exists(self.file_name):
                os.remove(self.file_name)

            write_file = open(self.file_name, 'w')
            write_file.write(content)
            write_file.close()

            tmpfile.close()
        else:
            print "file %s not found" % self.file_name
