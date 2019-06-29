#!/usr/bin/python3.5
# -*-coding:utf-8 -*

import subprocess
child = subprocess.Popen("uname -a | grep Ubuntu", shell=True, stdout=subprocess.PIPE)
streamdata = child.communicate()[0]
rc = child.returncode
if child.returncode != 0:
    print('cest du init')

if child.returncode is not '0':
    print('cest du string')

if child.returncode == 1:
    print('cest du init ok')

if child.returncode is '1':
    print('cest du string ok')



