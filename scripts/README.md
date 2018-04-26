## submit.py

You can use this to send jobs, local or lxplus batch. Proper folders will be automatically created. N.B.: Can also be imported and used as a function.

Running ```python submit.py -h``` will give you a fill set of options.

Exaple command:

```
python submit.py -d main_job_folder -n subjob_name_name "Your command as you would send it in the shell" -fi [List or files to copy over]
```

Adding a ```--local``` option makes it run in local. Runs in batch my default.

Exaple commands:

```
python submit.py -d myjob -n 0 'python myscrip.py' -fi myinput.txt
python submit.py -d myjob_bash -n 0 --local './mybash_scrupt.sh' -fi myinput.root
python submit.py -s 'lb-run DaVinci/latest bash' -d myotherjob -n 0 --local 'python job.py'
```

## check_jobs.py

Will check jobs status on LSF, lxlplus batch system. N.B.: Can also be imported and used as a function.

Exaple command: ```python check_jobs.py -j somename```

It will look for all jobs containing "somename" in their names and record their status. The output will be a dictionary of this kind: {"RUN":10,"PEND":3}.

A function is_job_done() is also provided, which returns true with the dictionary is empty, namely no jobs with that name are running or pending.

## remote_ls.py

This script allows you to easily "ls" eos from anywhere XRootD is installed. N.B.: Can also be imported and used as a function.

Exaple command: ```python remotels.py -p /eos/lhcb/user/{u}/{user}/```

N.B.: The good thing here is that this works also when you are not on lxplus. E.g. In Docker containers or local clusters. So this allows you to generalise where your analysis is run. When importing it the function works both in python2 and python3 environments.




