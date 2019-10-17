#!/usr/bin/python3
#-*- coding: utf-8 -*-

from flask import Flask, render_template, request, abort, Response, session, url_for, redirect, jsonify
import pymysql
import datetime, re, os, random, json, urllib.parse, urllib.request



app = Flask(__name__)
db = pymysql.connect(host="localhost", user="root", password="", database="mydb", charset="utf8")
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT uname, pub_time, content, topic, mid FROM mb_user, mb_message WHERE mb_user.uid = mb_message.uid")
        res = cur.fetchall()
        cur.close()        
        return render_template('zhuye.html', contents=res)

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
            if 0 < len(content) <= 500:
                # 将留言保存到数据库
                uid = user_info.get("uid")
                pub_time = datetime.datetime.now()
                from_ip = request.remote_addr

                try:
                    cur = db.cursor()
                    cur.execute("INSERT INTO mb_message (uid, content, pub_time, from_ip, topic) VALUES (%s, %s, %s, %s, %s)", (uid, content, pub_time, from_ip, topic ))
                    cur.close()
                    db.commit()
                    return redirect(url_for("home"))
                except Exception as e:
                    print(e)
                    
        abort(Response("发帖失败！"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        uname = request.form.get("userName")
        upass = request.form.get("password")
        # if not (uname and uname.strip() and upass and upass.strip()):
        #     abort(Response("登录失败！"))

        # if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
        #     abort(Response("用户名不合法！"))

        # # 密码长度介于6-15
        # if not (len(upass) >= 6 and len(upass) <= 15):
        #     abort(Response("密码不合法！"))    
        
        cur = db.cursor()
        cur.execute("SELECT * FROM mb_user WHERE uname=%s", (uname))
        res = cur.fetchone()
        cur.close()

              
        if res:
            # 登录成功就跳转到用户个人中心


            session["user_info"] = {
                "uid": res[0],
                "uname": res[1],
                "upass": res[2],
                "email": res[3],
            }

            return redirect(url_for("home"))
            # return render_template("zhuye.html")
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
        cur = db.cursor()
        cur.execute("SELECT uid FROM mb_user WHERE uname=%s", (uname,))
        res = cur.rowcount
        cur.close()
        if res != 0:
            abort(Response("用户名已被注册！"+"<br>"+"<a href=\"reg\">点击返回注册页面</a>"))

        try:
            cur = db.cursor()
            cur.execute('INSERT INTO mb_user (uname, upass, email) VALUES ("%s", %s, "%s")'%(uname, upass, email))
            cur.close()    
            db.commit()
            return render_template("zhuye.html")
        except:
            abort(Response("用户注册失败！"))

@app.route("/logout")
def logout_handle():
    if session.get("user_info"):
        session.pop("user_info")
    return redirect(url_for("home"))

@app.route("/neirong/<post_id>", methods=["GET","POST"])
def neirong_template(post_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM mb_message WHERE mid= '%s' " %(post_id))
    res1 = cur.fetchone()
    cur.close()

    if res1:
        session["reply_info"] = {
            "mid": res1[0],
            "uid": res1[1],
        }
    print(res1)
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT uname, pub_time, content, topic, mid FROM mb_user, mb_message WHERE mb_user.uid = mb_message.uid and mid = '%s' " %(post_id))
        res = cur.fetchall()
        cur.close()
        cur = db.cursor()
        cur.execute("SELECT pub_time, reply,  r_pub_time, uname FROM mb_user ,mb_reply, mb_message  WHERE mb_message.mid = mb_reply.mid and mb_user.uid = mb_reply.uid and mb_message.mid = '%s' " %(post_id) )
        res2 = cur.fetchall()
        cur.close()

        # return render_template("neirong.html", contents=res)
        return render_template("neirong.html", contents=res, replys=res2)
        # return render_template(url_for("neirong_template", post_id=post_id), contents=res, replys=res2)
    if request.method == "POST":
        user_info = session.get("user_info")
        reply_info = session.get("reply_info")
        reply = request.form.get("reply")
        print(reply, reply_info)


        if reply:
            reply = reply.strip()
            if 0 < len(reply) <= 500:
                # 将留言保存到数据库
                uid = user_info.get("uid")
                mid = reply_info.get("mid")  
                r_pub_time = datetime.datetime.now()
                try:
                    cur = db.cursor()
                    cur.execute("INSERT INTO mb_reply (uid, mid, reply, r_pub_time) VALUES (%s, %s, %s, %s)", (uid, mid, reply, r_pub_time))
                    cur.close()
                    db.commit()

                    return redirect(url_for("neirong_template",post_id=mid))
                except Exception as e:
                    print(e)
                    
        abort(Response("发帖失败！"))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)

