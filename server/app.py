from flask import Flask, request, jsonify, abort, render_template
import socket
import json

# 챗봇 엔진 서버 정보
host = "127.0.0.1"      # 챗봇 엔진 서버 IP
port = 5050             # 챗봇 엔진 port

# Flask 애플리케이션
app = Flask(__name__)

# 챗봇 엔진 query 전송 API
@app.route('/query', methods=['POST'])
def query():
    body = request.get_json()
    try:
        # 일반 질의응답 API
        ret = {
            'Query' : 'test',
        }
        return jsonify(ret)

    except Exception as ex:
        # 오류 발생 시 500 Error
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)