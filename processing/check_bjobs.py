import os, argparse
import subprocess as sb

def check_jobs(jname) :
    
    out = str(sb.check_output(["bjobs"]))#,shell=True)
    d = {'RUN' : 0, 'PEND' : 0}
    for l in out.split('\n')[1:] :
        toks = l.split()
        if len(toks) < 6 : continue 
   
        status = toks[2]
        name   = toks[5]

        if jname is not None and jname not in name : continue

        if status in d.keys() : d[status] += 1
        else : d[status] = 1
    
    return d

def is_job_done(name) :

    d = check_jobs(name)

    if d['PEND'] == 0 and d['RUN'] == 0 :
        return True
    return False


if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument("-j","--jname",default = None)
    args = parser.parse_args()

    check_jobs(jname)





