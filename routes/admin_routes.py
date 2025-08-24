from flask import request, render_template, redirect, url_for, session, send_file
from datetime import datetime, timedelta
from io import BytesIO
from openpyxl import Workbook
from app import app
from db.models import Session, Application
import pytz
from utils.smtp_sender import notify_status_change_direct
from flask import current_app

moscow_tz = pytz.timezone('Europe/Moscow')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'admin' not in session:
        return redirect(url_for('login'))

    db_session = Session()
    if request.method == 'POST':
        app_id = request.form.get('id')
        record = db_session.query(Application).filter_by(id=app_id).first()
        if record:
            record.status = request.form.get('status')
            record.note = request.form.get('note')
            db_session.commit()
            if record.email:
                notify_status_change_direct(current_app, record.email, record.id, record.status, record.note, record.description)
        return redirect(url_for('admin_panel'))

    query = db_session.query(Application)
    filters = {k: request.args.get(k, '') for k in ['status', 'name', 'department', 'from_date', 'to_date']}

    if filters['status']:
        query = query.filter(Application.status.ilike(f"%{filters['status']}%"))
    if filters['name']:
        query = query.filter(Application.name.ilike(f"%{filters['name']}%"))
    if filters['department']:
        query = query.filter(Application.department.ilike(f"%{filters['department']}%"))
    if filters['from_date']:
        try:
            # Создаем дату в московском времени
            from_date = moscow_tz.localize(datetime.strptime(filters['from_date'], "%Y-%m-%d"))
            query = query.filter(Application.submitted_at >= from_date)
        except ValueError:
            pass
    if filters['to_date']:
        try:
            # Создаем дату в московском времени + 1 день
            to_date = moscow_tz.localize(datetime.strptime(filters['to_date'], "%Y-%m-%d") + timedelta(days=1))
            query = query.filter(Application.submitted_at < to_date)
        except ValueError:
            pass

    records = query.order_by(Application.submitted_at.desc()).all()
    db_session.close()
    return render_template('admin_panel.html', records=records, filters=filters, moscow=moscow_tz)

@app.route('/admin/export')
def export_excel():
    if 'admin' not in session:
        return redirect(url_for('login'))

    db_session = Session()
    query = db_session.query(Application)
    for k in ['status', 'name', 'department']:
        v = request.args.get(k, '')
        if v:
            query = query.filter(getattr(Application, k).ilike(f"%{v}%"))

    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')

    if from_date:
        try:
            from_date_tz = moscow_tz.localize(datetime.strptime(from_date, "%Y-%m-%d"))
            query = query.filter(Application.submitted_at >= from_date_tz)
        except ValueError:
            pass
    if to_date:
        try:
            to_date_tz = moscow_tz.localize(datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1))
            query = query.filter(Application.submitted_at < to_date_tz)
        except ValueError:
            pass

    records = query.order_by(Application.submitted_at.desc()).all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Заявки"
    ws.append(["ID", "ФИО", "Должность", "Описание", "Стоимость", "Телефон", "Email",
               "Филиал", "Файл", "Дата подачи", "Статус", "Примечание", "Рейтинг"])
    for r in records:
        ws.append([r.id, r.name, r.position, r.description, r.cost, r.phone, r.email, r.department,
                   r.file_url, r.submitted_at.strftime('%Y-%m-%d %H:%M') if r.submitted_at else '',
                   r.status, r.note or '', round(r.rating or 0, 1)])
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    db_session.close()
    return send_file(output, download_name="zayavki.xlsx", as_attachment=True,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")