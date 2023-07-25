from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from datetime import date

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=f"postgresql://{'postgres'}:{'Shiva09'}@{'localhost'}:{'5432'}/{'ecommerce'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class EmpDutyAssociation(db.Model):
    __tablename__ = 'emp_duties'
    ed_id=db.Column(db.Integer,primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('emp.id'))
    duty_id = db.Column(db.Integer, db.ForeignKey('duty.id'))

    # Define the relationships with User and Role models
    emp = db.relationship('Emp', back_populates="duties")
    duty = db.relationship('Duty', back_populates="emps")

    def __init__(self,emp_id,duty_id):
        self.emp_id=emp_id
        self.duty_id=duty_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Emp(db.Model):
    __tablename__ = 'emp'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    duties = db.relationship('EmpDutyAssociation', back_populates='emp',  cascade='all, delete-orphan') # Add passive_deletes=True

    def __init__(self,emp_name):
        self.name=emp_name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Duty(db.Model):
    __tablename__ = 'duty'
    id = db.Column(db.Integer, primary_key=True)
    duty_name = db.Column(db.String(30))
    emps = db.relationship('EmpDutyAssociation', back_populates='duty',  cascade='all, delete-orphan') # Add passive_deletes=True

    def __init__(self,duty_name):
        self.duty_name = duty_name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/api/InsertEmployee",methods=['POST'])
def insert_employee():
    data=request.get_json()
    name=data["name"]
    emp=Emp(name)
    db.session.add(emp)
    db.session.commit()
    emp.query.all()
    return jsonify(emp.as_dict())

@app.route("/api/InsertDuty",methods=['POST'])
def insert_duty():
    data=request.get_json()
    duty_name=data["duty_name"]
    duty=Duty(duty_name)
    db.session.add(duty)
    db.session.commit()
    duty.query.all()
    return jsonify(duty.as_dict())

@app.route("/api/InsertEmpDuty",methods=['POST'])
def insert_emp_duty():
    data=request.get_json()
    emp_id=data["emp_id"]
    duty_id=data["duty_id"]
    emp_duty=EmpDutyAssociation(emp_id,duty_id)
    db.session.add(emp_duty)
    db.session.commit()
    EmpDutyAssociation.query.all()
    return jsonify(emp_duty.as_dict())

@app.route("/api/DeleteEmp",methods=['POST'])
def delete_emp():
    data = request.get_json()
    emp = Emp.query.get(data['id'])
    if not emp:
        return jsonify({"message": f"User with ID {data['id']} not found"}), 404
    try:
        db.session.delete(emp)
        db.session.commit()
        return jsonify({"message": f"User with ID {data['id']} has been deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error while deleting user with ID {emp.id}: {str(e)}"}), 500

@app.route("/api/DeleteDuty",methods=['POST'])
def delete_duty():
    data = request.get_json()
    duty = Duty.query.get(data['id'])
    if not duty:
        return jsonify({"message": f"Duty with ID {data['id']} not found"}), 404
    try:
        db.session.delete(duty)
        db.session.commit()
        return jsonify({"message": f"Duty with ID {data['id']} has been deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error while deleting user with ID {duty.id}: {str(e)}"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)