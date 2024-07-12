from flask_restful import reqparse, Resource
from app.models.insurance_claim_model import InsuranceClaim
from app import db

parser_insurance_claim = reqparse.RequestParser()
parser_insurance_claim.add_argument('patient_id', type=int, required=True, help='Patient ID cannot be blank')
parser_insurance_claim.add_argument('amount', type=float, required=True, help='Amount cannot be blank')
parser_insurance_claim.add_argument('status', type=str, required=True, help='Status cannot be blank')


class InsuranceClaimListResource(Resource):
    def get(self):
        insurance_claims = InsuranceClaim.query.all()
        return [claim.to_dict() for claim in insurance_claims], 200

    def post(self):
        args = parser_insurance_claim.parse_args()
        new_claim = InsuranceClaim(
            patient_id=args['patient_id'],
            amount=args['amount'],
            status=args['status']
        )
        db.session.add(new_claim)
        db.session.commit()
        return new_claim.to_dict(), 201


class InsuranceClaimResource(Resource):
    def get(self, id):
        claim = InsuranceClaim.query.get_or_404(id)
        return claim.to_dict(), 200

    def post(self):
        args = parser_insurance_claim.parse_args()
        new_claim = InsuranceClaim(
            patient_id=args['patient_id'],
            amount=args['amount'],
            status=args['status']
        )
        db.session.add(new_claim)
        db.session.commit()
        return new_claim.to_dict(), 201

    def put(self, id):
        args = parser_insurance_claim.parse_args()
        claim = InsuranceClaim.query.get_or_404(id)
        claim.patient_id = args.get('patient_id', claim.patient_id)
        claim.amount = args.get('amount', claim.amount)
        claim.status = args.get('status', claim.status)
        db.session.commit()
        return claim.to_dict(), 200

    def delete(self, id):
        claim = InsuranceClaim.query.get_or_404(id)
        db.session.delete(claim)
        db.session.commit()
        return '', 204
