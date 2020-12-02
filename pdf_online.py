import os
import time
import json
from flask import jsonify
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
UPLOAD_FOLDER = './static/doc'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
bootstrap = Bootstrap(app)




@app.route('/upload', methods=["GET", "POST"])
def upload_test():
    return render_template("upload.html")

#http://127.0.0.1:5000/show?filename=xxx
@app.route('/show', methods=["GET", "POST"])
def show_test():
    filename = request.args.get('filename',str)
    print(filename)
    filepath = UPLOAD_FOLDER + '/'+filename
    if os.path.exists(filepath):
        print(True)
        respath = "http://127.0.0.1:5000/static/pdfjs/web/viewer.html?file=/static/doc/"+ filename
        print(respath)
        return render_template("show.html",respath =respath)
    return render_template("show.html")


@app.route('/booklist', methods=["GET", "POST"])
def get_filelist():
    filepath = UPLOAD_FOLDER + '/'
    returnres = {"state": 200, "msg": "succsuful", "result": ""}
    if os.path.exists(filepath):
        filelist = os.listdir(filepath)
        print(filelist)
        returnres['result'] = filelist
    else:
        returnres['msg'] = 'filepath not exist'
    return jsonify(returnres)


@app.route("/api/upload", methods=["GET", "POST"])
def upload():
    file = request.files.get("file_data")
    msg = api_upload(app, file)
    upload_msg = json.loads(msg.data.decode("utf-8"))
    errmsg = upload_msg.get("errmsg")
    return jsonify({"msg": errmsg})


def api_upload(app_boj, file):
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
    file_dir = os.path.join(basedir, app_boj.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    filename = file.filename
    print(filename)
    file.save(os.path.join(file_dir, filename))  #保存文件到upload目录
    return jsonify({"result": "上传成功", "filename": filename, "state": 200})


if __name__ == '__main__':
    app.run(debug=True)
