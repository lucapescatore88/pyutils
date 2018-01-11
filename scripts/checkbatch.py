import subprocess as sb
import sys, re, os

def check_jobs(jnames) :
    
    if isinstance(jnames,str) : jnames = [jnames]
    p = sb.Popen(["bjobs"],stdout=sb.PIPE,stderr=sb.PIPE)
    out, err = p.communicate() 
    
    of = open("test.txt",'w')
    out = '\n'.join(str(out).split('\\n'))
    of.write(out)
    of.close()

    d = {'RUN' : 0, 'PEND' : 0}
    for jname in jnames :
        for l in out.split('\n')[1:] :
            toks = l.split()
            if len(toks) < 6 : continue 
   
            status = toks[2]
            name   = toks[5]

            if jname not in name : continue

            if status in d.keys() : d[status] += 1
            else : d[status] = 1
    
    return d

def is_job_done(name) :

    d = check_jobs(name)

    if d['PEND'] == 0 and d['RUN'] == 0 :
        return True
    return False

def wait_batch(jobs,callback=None) :       
        
    from time import sleep
    done = False
    while not done :
        done = True
        for j in jobs :
            done *= is_job_done(j)
        print('\rJobs are running or pending: use "bjobs" to have a look\r')
        sleep(1)
    if callback is not None : callback();

if __name__ == '__main__' :

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-j","--jname",default = None)
    args = parser.parse_args()

    check_jobs(jname)


