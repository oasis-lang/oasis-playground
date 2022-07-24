import os
import random
import subprocess
import base64
from flask import Flask, request, make_response, redirect, url_for

app = Flask(__name__, static_url_path='', static_folder='static')

command = "firejail --quiet --private=./ java -jar oasis.jar "

@app.route('/exec', methods=['POST'])
def exec_script():  # put application's code here
    name = 'f_' + str(random.randint(0, 1000000)) + '.oa'
    with open(name, 'w') as file:
        file.write(base64.b64decode(request.get_json()['code']).decode('utf-8'))
    result = ""
    try:
    	result = subprocess.check_output((command + name).split(' '), stderr=subprocess.STDOUT, timeout=60)
    except subprocess.CalledProcessError as e:
        result = e.output.decode('utf-8')
    os.remove(name)
    return make_response(result, 200)

@app.route('/')
def root():
	return redirect(url_for('static', filename='index.html'))

if __name__ == '__main__':
    app.run()
