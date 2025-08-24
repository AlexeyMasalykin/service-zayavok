from flask import request, render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

# Маршрут загрузки файлов отключен - используется только ручное заполнение
@app.route('/submit', methods=['GET', 'POST'])
def upload_file():
    # Редирект на ручное заполнение
    from flask import redirect, url_for
    return redirect(url_for('manual.manual_form'))

# Маршрут /upload/<filename> удален - файлы больше не загружаются

@app.route('/track', methods=['GET', 'POST'])
def track_application():
    from db.models import Session, Application
    record = None
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        if app_id and app_id.isdigit():
            session = Session()
            record = session.query(Application).filter_by(id=int(app_id)).first()
            session.close()
    return render_template('track.html', record=record)
