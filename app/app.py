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

app = Flask(__name__)

# ファイル容量上限 : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', \
		title = 'SB Online Judge', \
		message = 'ソースコードを選択して下さい。', \
		flag = False)

@app.route('/', methods=['POST'])
def post():
	
	# ファイルのリクエストパラメータを取得
	f = request.files.get('file')
	
	# ファイル名の決定
	filename = secure_filename(f.filename)
	timestamp = str(datetime.now().timestamp()).replace('.', '') + str(random.random())[-5: ]
	filename = timestamp + '.' + filename.split('.')[-1]	

	# language value 0: python, 1: c++
	lv = 0
	if(filename.split('.')[-1] != 'py'): lv = 1
	
	# ファイルを保存するディレクトリを指定
	filepath = 'static/file/' + filename
	
	# ファイルを保存する
	f.save(filepath)
	
	command = "python3 judge.py " + filepath + " 20"
	proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)

	# states = proc.get('stdout')
	# is_ac = True
	# for state in states:
	# 	if(state[0] != 1): is_ac = False

	return str(proc)

	# state = judge(filepath, 20)
	# print(state)
	# return str(state)
	
	
	# return render_template('index.html', \
	# 	title = 'Form Sample(post)', \
	# 	message = 'アップロードされた画像({})'.format(filename), \
	# 	flag = True, \
	# 	image_name = filename, \
	# 	image_url = filepath)

# @timeout_decorator.timeout(2.0)
# def process(filepath, i):
# 	print("2 ", end="")
# 	command = "python3 " + filepath + " < static/testcase/in/" + i + ".in > static/testcase/userout/out"
# 	proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
# 	print(proc)
# 	print("3 ", end="")

# class procClass:
# 	@timeout(MAIN_PROCESS_TIMEOUT)
# 	def main(self, filepath, i):
		
# 		command = "python3 " + filepath + " < static/testcase/in/" + i + ".in > static/testcase/userout/out"
# 		start = time.time()
# 		proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
# 		elapsed_time = time.time() - start

# 		return elapsed_time

# 	def clean_up(self):
# 		pass


# def judge(filepath, t):
# 	state = [0] * t # 0: WJ, 1: AC, 2: WA, 3: TLE
# 	for i in range(1, t+1):
# 		tle_cnt = 0
# 		while True:
# 			process = procClass()
# 			try:
# 				elapsed_time = process.main(filepath, str(i))
# 				if(elapsed_time > 2.0): raise TimeoutError
# 				break

# 			except TimeoutError:
# 				tle_cnt += 1


# 			if(tle_cnt == 3):
# 				state[i-1] = 3
# 				break
		
# 		if(filecmp.cmp("static/testcase/out/" + str(i) + ".out", "static/testcase/userout/out")):
# 			state[i-1] = 1
# 		else:
# 			state[i-1] = 2

# 	return state

		
if __name__ == '__main__':
	app.run(debug=True)