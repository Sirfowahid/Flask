from flask import Blueprint, render_template,redirect,url_for,session,request
from app.database.models import db

main_bp = Blueprint('main_bp',__name__)


@main_bp.route('/')
def index(): 
    return render_template('index.html')

