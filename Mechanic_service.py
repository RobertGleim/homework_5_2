from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Float, String, Date, Integer, ForeignKey
from datetime import date
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError



# customers: name, email. phone, address, id
# service tickets, id, cutomers, mechanics, service disc, price, vin
# mechanics: username, password, email, salary, address, id




app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mechanic.db'



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

db.init_app(app)
ma.init_app(app)

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
    price: Mapped[float] = mapped_column(Float,nullable=False)
    vin: Mapped[str] = mapped_column(String(20), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, default=lambda: date.today(), nullable=False)

    
    
    mechanics: Mapped[list['Ticket_Mechanics']] = relationship('Ticket_Mechanics', back_populates='service_ticket')
    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    
    
class Ticket_Mechanics(Base):
    __tablename__ = 'ticket_mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(Integer,ForeignKey('service_tickets.id'), nullable=False)
    mechanic_id: Mapped[int] = mapped_column(Integer,ForeignKey('mechanics.id'), nullable=False)
    service_ticket: Mapped['Service_Ticket'] = relationship('Service_Ticket', back_populates='mechanics')
    mechanic: Mapped['Mechanics'] = relationship('Mechanics', back_populates='service_tickets')

    
     
      
    
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
    
    
    
    
class  CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
       
service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)


class Ticket_MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket_Mechanics
        
ticket_mechanic_schema = Ticket_MechanicSchema()
ticket_mechanics_schema = Ticket_MechanicSchema(many=True)

class MechanicsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        
mechanic_schema = MechanicsSchema()
mechanics_schema = MechanicsSchema(many=True)

    
    
    
#====================================== crud operations =========================================

@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages),400

    new_customer = Customers(**data)
    db.session.add(new_customer)
    db.session.commit()
    print(f"New User was created, Welcome: {new_customer.first_name} {new_customer.last_name}")
    return customer_schema.jsonify(new_customer), 201

@app.route('/customers', methods=['GET'])
def read_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200

@app.route('/customers/<int:customer_id>', methods=['GET'])
def read_customer(customer_id):
    customer = db.session.get(Customers, customer_id) 
    print(f"Customer found: {customer.first_name} {customer.last_name}")
    return customer_schema.jsonify(customer), 200



@app.route('/customers/<int:customers_id>', methods=['DELETE'])  
def delete_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    db.session.delete(customer)
    db.session.commit()
    print(f"Customer deleted: {customer.first_name} {customer.last_name}")
    return jsonify({"message": f"Sorry to see you go! {customers_id}"}), 200

# @app.route('/customers/<int:customer_id>', methods=['PUT'])
# def update_customer(customer_id):
#     customer = db.session.get(Customers, customer_id)
#     db.session.append(customer)
#     db.session.commit()
#     print(f"Customer updated: {customer.first_name} {customer.last_name}")
#     return customer_schema.jsonify(customer), 200

    



        
    

with app.app_context():
    db.create_all()        
        
app.run(debug=True)        

# =================================================================================================
    # python -m venv venv
    # venv\Scripts\activate
    # pip install flask-marshmallow
    # pip install marshmallow-sqlalchemy
    # pip install flask-sqlalchemy
    # pip install -r requirements.txt
    # pip freeze > requirements.txt
    # app.run(debug=True)  
# =================================================================================================