from db.models import Application, Session

def save_to_db(fields, link, rating=0.0):
    initiator = fields.get('initiator', '')
    parts = [p.strip() for p in initiator.split(',', 1)]
    name, position = parts if len(parts) == 2 else (initiator, '')

    app = Application(
        name=name,
        position=position,
        description=fields['description'],
        cost=fields['cost'],
        phone=fields['phone'],
        email=fields['email'],
        department=fields['department'],
        file_url=link,
        rating=rating
    )
    session = Session()
    session.add(app)
    session.commit()
    session.refresh(app)
    session.close()
    return app.id