from flask import request
from flask_restx import Resource, fields
from flaskr.namespaces import nutrizionista_ns
from flaskr.services.nutrizionista_service import NutrizionistaService
from flaskr.limiter_config import limiter
from flaskr.utils.jwt_custom_decorators import nutrizionista_required
from flask_jwt_extended import  get_jwt_identity


login_nutrizionista = nutrizionista_ns.model('nutrizionista', {
    'password': fields.String('password of the nutrizionista'),
    'email': fields.String('email of the nutrizionista')
})

signup_paziente_from_nutrizionista = nutrizionista_ns.model('paziente da registrare', {
    'email': fields.String('mail of the paziente', required=True)
}, strict = True) 

class NutrizionistaLogin(Resource):

    @limiter.limit("40/day; 15/hour; 5/minute; 1/second")
    @nutrizionista_ns.expect(login_nutrizionista)
    @nutrizionista_ns.doc('login nutrizionista')
    def post(self):
        data = request.get_json()
        return NutrizionistaService.login_nutrizionista(data['email'], data['password'], data)

class NutrizionistaPaziente(Resource):
    
    @nutrizionista_required()
    @nutrizionista_ns.expect(signup_paziente_from_nutrizionista)
    @nutrizionista_ns.doc('create paziente')
    def post(self):
        s_paziente = request.get_json()        
        # Chiamata al service per la registrazione del paziente
        return NutrizionistaService.register_paziente(s_paziente, get_jwt_identity())
          