from flask import Blueprint, Flask,flash, sessions, request, render_template, redirect, url_for, send_from_directory, send_file, safe_join, abort,current_app
from flask_login import login_required, current_user
import os
from . import db
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_dropzone import Dropzone
from flask_mail import Mail, Message

cloud = Blueprint('cloud', __name__)
dropzone = Dropzone(current_app)
mail = Mail(current_app)

def list_files():
    files = []
    for filename in os.listdir("/home/mohamedaziz/files/"+current_user.email):
        files.append(filename)
    return files


@cloud.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join("/home/mohamedaziz/files/"+current_user.email, secure_filename(f.filename)))
    return redirect(url_for('main.profile'))


@cloud.route("/download/<file>")
@login_required
def getfile(file):
    path = "/home/mohamedaziz/files/"+current_user.email+"/"
    return send_from_directory(path, filename=file, as_attachment=True)


@cloud.route("/show/<file>")
@login_required
def show(file):
    path = "/home/mohamedaziz/files/"+current_user.email+"/"
    return send_from_directory(path, filename=file, as_attachment=False)


@cloud.route("/delete/<file>")
@login_required
def delete(file):
    path = "/home/mohamedaziz/files/"+current_user.email+"/"
    os.remove(os.path.join(path, file))
    return redirect(url_for('main.profile'))

@cloud.route("/mail/<file>")
@login_required
def Mail(file):
    msg = Message('Requested File', sender='yesyes02000@gmail.com', recipients=[current_user.email])
    msg.body = 'Your file'
    with current_app.open_resource("/home/mohamedaziz/files/"+current_user.email+"/"+file) as fp:
      msg.attach(file,'application/octect-stream', fp.read())
    mail.send(msg)
    flash('Mail sent')
    return redirect(url_for('main.profile'))