## submit.py

You can use this to send jobs, local or lxplus batch. Proper folders will be automatically created.
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