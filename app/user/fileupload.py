from datetime import datetime

from app.model import *
from app.user import *
from app.utils import *


@user.route('/file/add', methods=['POST'])
@user_login
def userFileAdd(token):
    userId = r.get(token)
    user = User.query.get(userId)
    files = request.files.getlist('files')
    if files is None:
        return jsonify(Error1004())
    try:
        for file in files:
            if len(file.filename) >= 255:
                return jsonify(Error1004())
            oldfilename = file.filename
            file.filename = random_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
            time = datetime.now().strftime('%Y-%m-%d %H:%M')
            db.session.add(UserFile(oldfilename=oldfilename, filename=file.filename, user_id=user.id, time=time))
    except:
        return jsonify(Error1003())
    db.session.commit()
    return jsonify(EventOK(token=token))


@user.route('/file/delete', methods=['POST'])
@user_login
def userFileDelete(token):
    userId = r.get(token)
    user = User.query.get(userId)
    fileId = request.form.get('fileid')
    file = UserFile.query.get(fileId)
    if file is None or file.user_id != user.id:
        return jsonify(Error1004())
    db.session.delete(file)
    db.session.commit()
    return jsonify(EventOK(token=token))


@user.route('/file/view', methods=['POST'])
@user_login
def userFileView(token):
    userId = r.get(token)
    user = User.query.get(userId)
    files = [
        {
            'fileid': file.id,
            'filename': file.oldfilename,
            'time': file.time,
            'downloadURL': 'http://' + HOST + '/admin/carousel/picture/' + file.filename
        }
        for file in user.files
    ]
    return jsonify(EventOK(token=token, files=files))


@user.route('/file/download/', methods=['POST'])
@user_login
def userFileDownLoad(token):
    userId = r.get(token)
    user = User.query.get(userId)
    fileId = request.form.get('fileid')
    file = UserFile.query.get(fileId)
    if file is None or file.user_id != user.id:
        return jsonify(Error1004())
    return send_from_directory(current_app.config['UPLOAD_PATH'], file.filename, as_attachment=True)
