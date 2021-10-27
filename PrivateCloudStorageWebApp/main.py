from flask import Blueprint, render_template, abort, jsonify, send_from_directory
from . import db
from flask_login import login_required, current_user
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


def list_files():
    files = []
    for filename in os.listdir("/home/mohamedaziz/files/"+current_user.email):
        files.append(filename)
    return files


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    fileslist = list_files()
    l = len(fileslist)
    path = "/home/mohamedaziz/files/"+current_user.email+"/"
    return render_template('profile.html', **locals())
