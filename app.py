import os, sys
import argparse
from pyfiglet import figlet_format

parser = argparse.ArgumentParser(description='SQLIA detection via reverse proxy', epilog='example: python '+os.path.basename(__file__)+' localhost 8000')
parser.add_argument('host', metavar='host', type=str, help='ip address of the server')
parser.add_argument('port', metavar='port', type=str, help='port number of the server')
args = parser.parse_args()

HOST = args.host
PORT = args.port

if HOST == '' or PORT == '':
    print('please specify a server host and port')
    sys.exit()

SOCKET = "http://" + HOST + ":" + PORT + "/"
TOKENS = ['"', "'", ';', '=', '-', '--', '/', '`', '~']

banner = figlet_format('SQLIA Guardian')
print(banner)

from flask import Flask, request, redirect, url_for
from flask_ipban import IpBan
from requests import get, put, post
from markupsafe import escape

app = Flask(__name__)
ip_ban = IpBan()
ip_ban.init_app(app)
ip_ban.ban_seconds = 6
ip_ban.ban_count = 1

@app.route('/')
def index():
    title = b'<h1 align="center"> VIA PROXY </h1>'
    payload = request.args.to_dict()
    ip_addr = request.remote_addr
    if sql_detect(payload, ip_addr): 
        return redirect(url_for('sql_message'))
    content = title + get(f'{SOCKET}', params=payload).content
    return content

@app.route('/<path:path>')
def insert(path):
    title = b'<h1 align="center"> VIA PROXY </h1>'
    payload = request.args.to_dict()
    ip_addr = request.remote_addr
    if sql_detect(payload, ip_addr): 
        return redirect(url_for('sql_message'))
    content = title + get(f'{SOCKET}{path}', params=payload).content
    return content

@app.route('/injection')
def sql_message():
    return '<h1 align="center">SQL INJECTION DETECTED</h1>'

def sql_detect(payload, ip_addr):
    for key in payload:
        for token in TOKENS:
            current = payload[key]
            if current.find(token) != -1:
                ip_ban.add(ip_addr)
                return True
    return False

if __name__ == '__main__':
    host = '0.0.0.0'
    port = '5000'
    app.run(host=host, port=port, debug=False)
