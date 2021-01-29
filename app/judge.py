# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import random
import subprocess
from subprocess import PIPE
import time
from timeout_decorator import timeout, TimeoutError
import filecmp
MAIN_PROCESS_TIMEOUT = 3
import sys
filepath = sys.argv[1]
t = int(sys.argv[2])


class procClass:
    @timeout(MAIN_PROCESS_TIMEOUT)
    def main(self, filepath, i):
		
        command = "python3 " + filepath + " < static/testcase/in/" + i + ".in > static/testcase/userout/out"
        start = time.time()
        proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
        # print(proc)
        elapsed_time = time.time() - start

        return elapsed_time

    def clean_up(self):
        pass

if __name__ == '__main__':
    
    state = [[0] * 2 for _ in range(t)] # 0: WJ, 1: AC, 2: WA, 3: TLE
    for i in range(1, t+1):
        tle_cnt = 0
        while True:
            process = procClass()
            try:
                elapsed_time = process.main(filepath, str(i))
                if(elapsed_time > 2.0): raise TimeoutError
                break

            except TimeoutError:
                tle_cnt += 1

            if(tle_cnt == 3):
                state[i-1][0] = 3
                state[i-1][1] = 2.2
                break

        if(filecmp.cmp("static/testcase/out/" + str(i) + ".out", "static/testcase/userout/out")):
            state[i-1][0] = 1
            state[i-1][1] = elapsed_time
        else:
            state[i-1][0] = 2
            state[i-1][1] = elapsed_time

    for i in range(1, t+1):
        print(i, state[i-1][0], state[i-1][1])