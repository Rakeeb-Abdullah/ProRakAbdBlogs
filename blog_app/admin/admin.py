from flask import Blueprint,render_template,redirect,request,Response
from flask_admin.contrib.sqla import ModelView
from blog_app import db,admin_,basic_auth
from blog_app.models import BlogPost,Admin_User,User
from werkzeug.exceptions import HTTPException

admin_con = Blueprint("admin_con", __name__, template_folder='template',static_folder='static')


class AdminView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'} ))

admin_.add_view(AdminView(BlogPost, db.session))
admin_.add_view(AdminView(Admin_User, db.session))
admin_.add_view(AdminView(User, db.session))

