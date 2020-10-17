from werkzeug.security import generate_password_hash, check_password_hash

from app import db
import hashlib
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    files = db.relationship("UserFile", backref='user')


    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def makeToken(self):
        md5 = hashlib.md5()
        temp = self.username + str(datetime.now().timestamp())
        md5.update(temp.encode('utf8'))
        token = md5.hexdigest()
        return token


class UserFile(db.Model):
    __tablename__ = 'userfile'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
