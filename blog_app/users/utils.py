import secrets
import os
from PIL import Image
from flask import url_for
from flask_mail import Message
from blog_app import mail,app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.relpath(os.path.join(app.root_path, 'static/profile_pics', picture_fn))

    output_size = (180, 180)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request for ProRakAbd BLOGS',
                    sender='noreply.prorakabd@gmail.com',
                    recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
{url_for('users.reset_token',token=token, _external=True)}

If you didn't request this reset please ignore,No changes will be made
*This is a system generated mail, Do not reply.
'''
    mail.send(msg)