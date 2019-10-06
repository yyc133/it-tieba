#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template


app = Flask(__name__)
app.config

@app.route("/", methods=["GET"])
def yreg():
    return render_template("reg.html")




if __name__ == "__main__":
    app.run(port=80,debug=True)
