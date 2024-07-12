from flask_restful import Resource, reqparse
from app.models.invoice_model import Invoice
from app import db

parser_invoice = reqparse.RequestParser()
parser_invoice.add_argument('patient_id', type=int, required=True, help='Patient ID cannot be blank')
parser_invoice.add_argument('amount', type=float, required=True, help='Amount cannot be blank')
parser_invoice.add_argument('description', type=str)



class InvoiceListResource(Resource):
    def get(self):
        invoices = Invoice.query.all()
        return [invoice.to_dict() for invoice in invoices], 200

    def post(self):
        args = parser_invoice.parse_args()
        new_invoice = Invoice(
            patient_id=args['patient_id'],
            amount=args['amount'],
            description=args.get('description')
        )
        db.session.add(new_invoice)
        db.session.commit()
        return new_invoice.to_dict(), 201


class InvoiceResource(Resource):
    def get(self, id):
        invoice = Invoice.query.get_or_404(id)
        return invoice.to_dict(), 200

    def post(self):
        args = parser_invoice.parse_args()
        new_invoice = Invoice(
            patient_id=args['patient_id'],
            amount=args['amount'],
            description=args.get('description')
        )
        db.session.add(new_invoice)
        db.session.commit()
        return new_invoice.to_dict(), 201


