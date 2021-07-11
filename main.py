from flask import Flask, render_template, request
import hashlib
import xmltodict
import time

app = Flask(__name__)

@app.route('/')
def get_index():
    res = '<p>xiongguoqing</p>'
    return res

@app.route('/wx', methods=["GET", "POST"])
def wx():
    if request.method == 'GET':
        signature=request.args.get('signature')
        timestamp=request.args.get('timestamp')
        nonce=request.args.get('nonce')
        echostr=request.args.get('echostr')
        token = "xiong"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode('utf-8'))
        sha1.update(list[1].encode('utf-8'))
        sha1.update(list[2].encode('utf-8'))
        hashcode = sha1.hexdigest()
        print ("handle/GET func: hashcode, signature, timestamp, nonce, echostr, token: ", hashcode, signature,timestamp,nonce,echostr)
        if hashcode == signature:
            return echostr
        else:
            return ""
    elif request.method == 'POST':
        xml_str = request.data
        if not xml_str:
            return ""
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")
        
        msg_type = xml_dict.get("MsgType")
        if msg_type == 'text':
            resp_dict = {
                'xml':{
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "you say:" + xml_dict.get("Content")
                    }
                }
        resp_xml_str = xmltodict.unparse(resp_dict)
        return resp_xml_str

if __name__ == '__main__':
    app.run(port='5000')

