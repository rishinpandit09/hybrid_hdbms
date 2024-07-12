from flask_restful import Resource, reqparse

from app import db
from app.models.employee_model import Employee

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
parser.add_argument('role', type=str, required=True, help='Role cannot be blank')
parser.add_argument('department', type=str)


class StaffListResource(Resource):
    def get(self):
        employees = Employee.query.all()
        return [employee.to_dict() for employee in employees], 200

    def post(self):
        args = parser.parse_args()
        new_employee = Employee(
            name=args['name'],
            role=args['role'],
            department=args.get('department')
        )
        db.session.add(new_employee)
        db.session.commit()
        return new_employee.to_dict(), 201


class StaffResource(Resource):
    def get(self, id):
        employee = Employee.query.get_or_404(id)
        return employee.to_dict(), 200

    def put(self, id):
        args = parser.parse_args()
        employee = Employee.query.get_or_404(id)
        employee.name = args.get('name', employee.name)
        employee.role = args.get('role', employee.role)
        employee.department = args.get('department', employee.department)
        db.session.commit()
        return employee.to_dict(), 200

    def delete(self, id):
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204
