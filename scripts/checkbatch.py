import subprocess as sb
import sys, re, os

def check_jobs(jnames) :
    
    if isinstance(jnames,str) : jnames = [jnames]
    out = sb.check_output('bjobs -o "JOBID:10 STAT:5 JOB_NAME:40"',shell=True)
    if sys.version_info.major >= 3. : out = out.decode('utf-8')
    
    d = {'RUN' : 0, 'PEND' : 0}
    for jname in jnames :
        for l in out.split('\n')[1:] :
            toks = l.split()
            if len(toks) < 3 : continue 
             
            status = toks[1]
            name   = toks[2]
            
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
        
    if isinstance(jobs, str): jobs=[jobs]

    from time import sleep
    done = False
    while not done :
        done = True
        ndone = 0 
        for j in jobs :
            cdone = is_job_done(j)
            done *= cdone
            if cdone : ndone += 1
        print( '\rRunning: %i jobs done over %i\r' % (ndone,len(jobs)) )
        sleep(1)
    if callback is not None : callback();

if __name__ == '__main__' :

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-j","--jname",default = None)
    args = parser.parse_args()

    print (check_jobs(args.jname))


