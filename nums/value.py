## Author: Luca Pescatore
## Mail: pluca@cern.ch

def get_str(num, scale=None, showscale=True, prec=None, otype='shell', showunit = True) :
        
        if scale is None : scale = 1

        #ownscale = detect_scale(num)
        nominal_value = num.nominal_value * 10**scale
        err = num.std_dev * 10**scale
        
        if prec is None :
            prec = 1
            if abs(err) < 0.5 :
                prec = abs(self.detect_scale()-scale)

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


def detect_scale(num) :

        scale = 0
        err = num.std_dev
        if abs(err) < 1.e-12 :
            return 0

        if num.std_dev < 1 :
            while err < 1. :
                err *= 10
                scale -= 1
        else :
            while err > 1. :
                err *= 0.1
                scale += 1
        
        return scale


def dict_errors(self, pattern=None, regex=None):
        '''
        Returns a dictionary with the various components of the errors
        a shell-like pattern or a regular espression can be given to reduce the components to select
        '''
        out = {}
        for key, value in self.error_components().items():
            tag = key.tag
            if out.has_key(tag): dd[tag] = sqrt(out[tag]**2+value**2)
            else : out[tag] = value

        if pattern:
            out = {key : value for key, value in dd.items() if fnmatch.fnmatch(key, pattern)}
        if regex:
            out = {key : value for key, value in dd.items() if re.match(regex, key)}

        return out


