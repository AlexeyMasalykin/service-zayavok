from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from sqlalchemy import Float
import pytz

Base = declarative_base()

# Московская временная зона
moscow_tz = pytz.timezone('Europe/Moscow')

def get_moscow_time():
    """Возвращает текущее время в московской временной зоне"""
    return datetime.now(moscow_tz)

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    position = Column(String(255))
    description = Column(Text)
    cost = Column(String(100))
    phone = Column(String(50))
    email = Column(String(100))
    department = Column(String(255))
    file_url = Column(Text)
    submitted_at = Column(DateTime, default=get_moscow_time)
    status = Column(String(100), default="новая")
    note = Column(Text)  # Примечания администратора
    ai_analysis = Column(Text)  # ИИ-анализ заявки
    rating = Column(Float)
    
    # Новые поля для ручного заполнения
    total_sum = Column(String(100))
    justification = Column(Text)
    is_manual = Column(Boolean, default=False)
    
    # Связь с элементами заявки
    items = relationship("ApplicationItem", back_populates="application", cascade="all, delete-orphan")

class ApplicationItem(Base):
    """Элементы таблицы в заявке"""
    __tablename__ = 'application_items'
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    item_name = Column(String(500), nullable=False)
    characteristics = Column(Text)
    unit = Column(String(50))
    quantity = Column(Integer)
    price = Column(Float)
    
    # Связь с заявкой
    application = relationship("Application", back_populates="items")

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)

def init_db():
    """Инициализация базы данных"""
    Base.metadata.create_all(engine)

