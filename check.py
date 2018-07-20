import sys
import os
import time
from queModel import queModel
PYTHON_SHELL_DIR = '/usr/bin/python3.6.2'
RUN_FILE_DIR = '/data/wwwroot/queue/cmd.py'
QUEUE_EXE_LOG_DIR = '/data/logs/queue/'

queue_num = queModel.notify_queue_num
queue_prefix = queModel.queue_prefix
arr = range(0, queue_num)
for x in arr:
    exe_args = queue_prefix + str(x)
    number = os.popen("ps -aux | grep '" + exe_args + "' | grep -v 'grep' | wc -l")
    number = int(number.read())
    if(number<1):
        cmd_str = 'nohup ' + PYTHON_SHELL_DIR + ' ' + RUN_FILE_DIR + ' ' + exe_args + ' >> ' + QUEUE_EXE_LOG_DIR + exe_args + '.log 2>&1 &'
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + cmd_str)
        os.system(cmd_str)