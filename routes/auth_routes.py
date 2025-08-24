from flask import request, render_template, redirect, url_for, session
import os
from app import app

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        error_message = "Неверный логин или пароль"
    return render_template('login.html', error=error_message)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))
