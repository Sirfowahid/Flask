from flask import Blueprint, render_template,redirect,url_for,session,request
from app.database.models import db

auth_bp = Blueprint('auth_bp',__name__)

@auth_bp.route('/real_time')
def real_time():
    return render_template('realtime.html')
