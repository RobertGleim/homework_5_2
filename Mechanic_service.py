from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, ForeignKey
from datetime import date

# customers: name, email. phone, address, id
# service tickets, id, cutomers, mechanics, service disc, price, vin
# mechanics: username, password, email, salary, address, id




app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mechanic.db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)

class Customers(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120),nullable=False,)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True) 
    
    service_tickets: Mapped[list['Service_Ticket']] = relationship('Service_Ticket', back_populates='customer') 
    
class Service_Ticket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)
    service_description: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    vin: Mapped[str] = mapped_column(String(20), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    
    mechanics: Mapped[list['Ticket_Mechanics']] = relationship('Ticket_Mechanics', back_populates='service_ticket')
    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    
    
class Ticket_Mechanics(Base):
    __tablename__ = 'ticket_mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(Integer,ForeignKey('service_tickets.id'), nullable=False)
    mechanic_id: Mapped[int] = mapped_column(Integer,ForeignKey('mechanics.id'), nullable=False)
    
     
      
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True) 
    
    service_tickets: Mapped[list['Ticket_Mechanics']] = relationship('Ticket_Mechanics', back_populates='mechanic')
    
  
    
    
with app.app_context():
    db.create_all()        
        
app.run()        
    