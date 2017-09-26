## Author: Luca Pescatore
## Mail: pluca@cern.ch
## Description: handles nominal_valueues with errors

import math
import uncertainties as unc

class Value(unc.core.Variable) :
    
    def __init__(self,val = 0,err = 0,unit=None, scale = 0):
        unc.core.Variable.__init__(self,val,err)
        self.scale = scale
        self.unit = unit

    def __repr__(self) :
        
        return self.get_str()

    def get_str(self, scale=None, showscale=True, prec=None, otype='shell', showunit = True) :
        
        if scale is None :
            scale = self.scale

        nominal_value = self.get_value(scale)
        err = self.get_err(scale)
        
        if prec is None :
            prec = 1
            if abs(err) < 0.5 :
                prec = abs(self.detect_scale()+self.scale-scale)

        pm    = '+/-'
        times = 'x'
        wrap  = ''
        exp = "10^{0:}".format(scale)
        if 'latex' in otype :
            pm    = r'\pm'
            times = r'\times'
            if 'nowrap' not in otype : wrap  = '$'
            exp = "10^{{"+"{0:}".format(scale)+"}}"

        out = ("{0:."+str(prec)+"f}").format(nominal_value)
        if err > 0 :
            out += (" {pm} {0:."+str(prec)+"f}").format(err,pm=pm)
        if scale != 0 and showscale :
            if err > 0 : out = '('+out+')'
            out += ' {times} {exp}'.format(prev=out,times=times,exp=exp)
        if self.unit is not None and showunit : 
            out += " "+self.unit 
        return wrap+out+wrap

    def set_scale(self,scale) :
        self.scale = scale

    def get_value(self, scale=0) :
        return self.nominal_value * 10**(self.scale-scale)

    def get_err(self,scale=0) :
        return self.std_dev * 10**(self.scale-scale)

    def change_scale(self,scale) :

        newval = self.nominal_value * 10**(self.scale-scale)
        newerr = self.std_dev * 10**(self.scale-scale)
        unc.core.Variable.__init__(self,newval,newerr)
        self.scale -= scale

    def change_unit(self,scale,unit) :

        newval = self.nominal_value * 10**(self.scale-scale)
        newerr = self.std_dev * 10**(self.scale-scale)
        unc.core.Variable.__init__(self,newval,newerr)
        self.unit = unit
    
    def auto_rescale(self) :

        self.detect_scale(True)
        self.unit = None

    def detect_scale(self,setscale=False) :

        scale = 0
        err = self.std_dev
        if abs(err) < 1.e-12 :
            return 0

        if self.std_dev < 1 :
            while err < 1. :
                err *= 10
                scale -= 1
        else :
            while err > 1. :
                err *= 0.1
                scale += 1
        
        if setscale :
            self.change_scale(scale)
        
        return scale



