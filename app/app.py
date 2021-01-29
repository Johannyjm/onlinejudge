# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import random
import subprocess
from subprocess import PIPE

app = Flask(__name__)

# ファイル容量上限 : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

@app.route('/', methods=['GET'])
def get():
	randomword = (
		'問題文', 
		'長さ N の数列Aが与えられます、l, r が Q 個与えられるので', 
		'a[l]〜a[r]の総和をQ行で出力してください。', 
		'---', 
		'制約', 
		'1 <= N <= 2*10^5', 
		'0 <= ai <= 10^9', 
		'1 <= Q <= 2*10^5', 
		'1 <= l <= r <= N', 
		'---', 
		'ソースコードを選択して下さい。( Python のみ)'
		)
	return render_template('index.html', \
		title = 'Online Judge', \
		randomword=randomword, \
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

	if(proc.returncode != 0):
		result = "RE"

	else:
		out = proc.stdout
		states = out.decode("UTF-8").split("\n")

		state_code = 0
		max_time = 0
		for state in states:
			state = state.split()
			if(len(state) != 3): continue
			
			if(state_code == 0 and state[1] == "2"): state_code = 1
			if(state[1] == "4"): state_code = 2
			max_time = max(max_time, float(state[2]))

		result = ["AC", "WA", "TLE"][state_code]
		result += " " + str(int(1000*round(max_time, 4))) + "ms"

	return render_template('index.html', \
		title = 'Online Judge', \
		message = result, \
		flag = True)

		
if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))