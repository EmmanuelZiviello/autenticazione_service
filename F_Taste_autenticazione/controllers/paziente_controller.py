from flask import request
from flask_restx import Resource, fields
from F_Taste_autenticazione.namespaces import paziente_ns
from F_Taste_autenticazione.services.paziente_service import PazienteService
from F_Taste_autenticazione.limiter_config import limiter
from F_Taste_autenticazione.utils.jwt_custom_decorators import paziente_required
from flask_jwt_extended import get_jwt_identity


cambio_password_model = paziente_ns.model('cambio password', {
    'password': fields.String('password of the paziente', required=True),
    'new_password': fields.String('new password', required=True)
}, strict=True)

recupero_password_model = paziente_ns.model('recupero password', {
    'id_paziente': fields.String('PAZ1324', required=True)
}, strict=True)

signup_paziente = paziente_ns.model('singup_paziente', {
    'password': fields.String('password of the paziente'),
    'email': fields.String('mail of the paziente'),
    'data_nascita': fields.String("format yyyy-MM-dd"),
    'sesso': fields.Boolean('true = maschio , false=femmina')
}, strict=True)

login_paziente = paziente_ns.model('paziente', {
    'password': fields.String('password of the paziente'),
    'email_paziente': fields.String('email of the paziente')
}, strict=True)

class PazienteLogin(Resource):
 

    @limiter.limit("40/day; 15/hour; 5/minute; 1/second")
    @paziente_ns.expect(login_paziente)
    @paziente_ns.doc('login paziente')
    def post(self):
        data = request.json
        return PazienteService.login_paziente(data['email_paziente'], data['password'])

class Paziente(Resource):
    @paziente_ns.expect(signup_paziente)
    @paziente_ns.doc('signup paziente')
    def post(self):
        s_paziente = request.get_json()        
        return PazienteService.register_paziente(s_paziente)
    

class PazientePassword(Resource):

    @paziente_required()
    @paziente_ns.expect(cambio_password_model) 
    @paziente_ns.doc('cambio password paziente')
    def put(self):
        json_data=request.get_json()
        id_paziente=get_jwt_identity()
        return PazienteService.cambio_pw_paziente(id_paziente,json_data)

    @limiter.limit("40/day; 15/hour; 5/minute; 1/second")
    @paziente_ns.expect(recupero_password_model)
    @paziente_ns.doc('il paziente riceve per email il link al password changer')
    def post(self):
        json_data=request.get_json()
        return PazienteService.recupero_pw_paziente(json_data)
