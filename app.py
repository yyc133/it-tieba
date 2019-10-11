#!/usr/bin/python3
#-*- coding: utf-8 -*-

from flask import Flask, render_template, request, abort, Response, session, url_for, redirect, jsonify
import pymysql
import datetime, re, os, random, json, urllib.parse, urllib.request
from flask_sqlalchemy import SQLAlchemy   


app = Flask(__name__)
db = pymysql.connect(host="localhost", user="root", password="yyc133", database="mydb", charset="utf8")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yyc133@127.0.0.1:3306/mydb?charset=utf8'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Mb_user(db.Model):
#     __tablename__ = "mb_user"
#     uid = db.Column(db.Integer, primary_key=True)
#     uname = db.Column(db.String(80), unique=True)
#     upass = db.Column(db.String(64), unique=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, uid, uname, upass, email):
#         self.uid = uid
#         self.uname = uname
#         self.upass = upass
#         self.email = email

#     def __repr__(self):
#         return '<mb_user %r>' % (self.uid, self.uname , self.upass , self.email)


app.secret_key = os.urandom(24)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("zhuye.html")
    elif request.method == "POST":
        user_info = session.get("user_info")
        # if not user_info:
        #     abort(Response("未登录！"))

        content = request.form.get("content")
        topic = request.form.get("topic")
        print(content,topic)
        if content and topic:
            content = content.strip()
            topic = topic.strip()
            if 0 < len(content) <= 200:
                # 将留言保存到数据库
                uid = user_info.get("uid")
                pub_time = datetime.datetime.now()
                from_ip = request.remote_addr

                try:
                    cur = db.cursor()
                    cur.execute("INSERT INTO mb_message (uid, content, pub_time, from_ip, topic) VALUES (%s, %s, %s, %s, %s)", (uid, content, pub_time, from_ip, topic ))
                    cur.close()
                    db.commit()
                    return "留言成功！"
                except Exception as e:
                    print(e)
                    
        abort(Response("留言失败！"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        uname = request.form.get("userName")
        upass = request.form.get("password")

        print(uname, upass)

        # if not (uname and uname.strip() and upass and upass.strip()):
        #     abort(Response("登录失败！"))

        # if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
        #     abort(Response("用户名不合法！"))

        # # 密码长度介于6-15
        # if not (len(upass) >= 6 and len(upass) <= 15):
        #     abort(Response("密码不合法！"))    
        
        cur = db.cursor()
        cur.execute("SELECT * FROM mb_user WHERE uname=%s", (uname,))
        res = cur.fetchone()
        cur.close()
        # res = Mb_user(uname, upass)
        # db.session.add(res)
        # db.session.commit()
        # return render_template("zhuye.html")
              
        if res:
            # 登录成功就跳转到用户个人中心


            session["user_info"] = {
                "uid": res[0],
                "uname": res[1],
                "upass": res[2],
                "email": res[3],
            }

            # return redirect(url_for("zhuye.html"))
            return render_template("zhuye.html")
        else:
            # 登录失败
            return render_template("/login", login_fail=1)

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("reg.html")
    elif request.method == "POST":
        email = request.form.get("email")
        uname = request.form.get("userName")
        upass = request.form.get("password")
        print(email, uname, upass)

        # stu = Mb_user(uname, upass, email)
        # db.session.add(stu)
        # db.session.commit()

        # return "注册成功！"


        cur = db.cursor()
        cur.execute("SELECT uid FROM mb_user WHERE uname=%s", (uname,))
        res = cur.rowcount
        cur.close()
        if res != 0:
            abort(Response("用户名已被注册！"+"<br>"+"5秒后自动跳回注册页面"+"<br>"+"<a href=\"reg\">点击返回注册页面</a>"))

        try:
            cur = db.cursor()
            sql = 'INSERT INTO mb_user (uname, upass, email) VALUES ("%s", %s, "%s")'% (uname, upass, email)
            print(sql)
            cur.execute(sql)
            cur.close()    
            db.commit()
            return render_template("zhuye.html")
        except:
            abort(Response("用户注册失败！"))

@app.route("/logout")
def logout_handle():
    if session.get("user_info"):
        session.pop("user_info")
    return render_template("zhuye.html")

if __name__ == '__main__':
    app.run(port=80, debug=True)

