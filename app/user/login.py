from app.model import *
from app.utils import *
from app.user import *


@user.route('/register', methods=['POST'])
def userRegister():
    username = request.form.get('username')
    password = request.form.get('password')
    if User.query.filter_by(username=username).first() is not None:
        return jsonify(Error1005())
    if len(username) >= 255 or len(password) >= 255:
        return jsonify(Error1004())
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    token = user.makeToken()
    r.set(token, str(user.id))
    return jsonify(EventOK(token=token))


@user.route('/login', methods=['POST'])
def userLogin():
    username = request.form.get('username')
    password = request.form.get('password')
    if len(username) >= 255 or len(password) >= 255:
        return jsonify(Error1004())
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(Error1001())
    if user.checkPassword(password) is not True:
        return jsonify(Error1002())
    token = user.makeToken()
    r.set(token, str(user.id))
    return jsonify(EventOK(token=token))


@user.route('/logout', methods=['POST'])
@user_login
def userLogout(token):
    try:
        r.delete(token)
        return jsonify(EventOK())
    except:
        return jsonify(Error1003())