# -*- coding:utf8 -*-
# author:yaolinxia
# datetime:2020/3/11
# software: PyCharm
from flask import Flask, request, jsonify, render_template
from flask_cors import cross_origin
from text_abstract import abstract

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.route('/summary', methods=["POST"])
@cross_origin()
def summary():
    try:
        input_title = request.form.get('title','')
        input_body = request.form.get('body','')
        # 调用摘要生成模型
        summary = abstract(input_body, input_title)
        result = {
            "data":{
                "content": summary
            }
        }
        # 转化成json文件
        return jsonify(result)
    except Exception as e:
        print(str(e.__traceback__))
        return jsonify({"data":str(e)})


if __name__ == '__main__':
    app.run()
application = app