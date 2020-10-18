from functools import wraps

from flask import request, jsonify

from app.extension import *

import os

import uuid

HOST = "127.0.0.1:5000"


def user_login(func):
    @wraps(func)
    def yes_or_no():
        token = request.form.get('token')
        if token is None:
            return jsonify(Error1004())
        if r.get(token) is None:
            return jsonify(Error1002())
        return func(token)

    return yes_or_no


def EventOK(**kwargs):
    data = {
        "status": 0,
        "data": kwargs
    }
    return data


# 对象不存在
def Error1001():
    message = {
        "status": 1001,
        "message": "对象不存在"
    }
    return message


# token/密码验证错误
def Error1002():
    message = {
        "status": 1002,
        "message": "token/密码验证错误"
    }
    return message


# 服务器错误
def Error1003():
    message = {
        "status": 1003,
        "message": "服务器错误"
    }
    return message


# 参数错误
def Error1004():
    message = {
        "status": 1004,
        "message": "参数错误"
    }
    return message


# 对象已存在
def Error1005():
    message = {
        "status": 1005,
        "message": "对象已存在"
    }
    return message


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename
