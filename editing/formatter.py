## Author: Luca Pescatore
## Mail: pluca@cern.ch
## Description: extends the standards string.format() to handle cases where the key is not present.

import string
from ROOT import *

class PartialFormatter(string.Formatter):

    '''
    You can use this object fo fill templates. On top of the normal format() it also deals with absent values

    Here an example

    from utils.formatter import PartialFormatter as Formatter
    fmt = Formatter()
    table = fmt.format(open("table_template.txt").read(),**some_dictionary)
    '''


    def __init__(self, missing='--', bad_fmt='!!'):
        self.missing, self.bad_fmt=missing, bad_fmt

    def get_field(self, field_name, args, kwargs):

        try:
            val=super(PartialFormatter, self).get_field(field_name, args, kwargs)
        except (KeyError, AttributeError):
            val=None,field_name
        return val

    def format_field(self, value, spec):
                # handle an invalid format
        if value==None: return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None: return self.bad_fmt
            else: raise


class Template():

    def __init__(self,fname) :
        self.fname = fname
        try :
            ifile = open(self.fname,'r')
            self.template = ifile.read()
        except :
            print "Cannot open file", self.fname

    def fill(self,data,ofile,opt = "") :

        out = open(ofile,'w')

        tmp = self.template
        if opt=="nospace" : tmp = self.template.replace(" ","")

        otext = PartialFormatter().format(tmp,**data)
        out.write(otext)
        out.close()
