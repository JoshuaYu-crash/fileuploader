from app.model import *
from app.utils import *
from app.user import *


@user.route('/file/add', methods=['POST'])
@user_login
def userFileAdd(token):
    pass


@user.route('/file/delete', methods=['POST'])
@user_login
def userFileDelete(token):
    pass


@user.route('/file/view', methods=['POST'])
@user_login
def userFileView(token):
    pass