from flask import request
from flask_restx import Resource, fields
from F_Taste_autenticazione.namespaces import paziente_ns
from F_Taste_autenticazione.services.paziente_service import PazienteService
from F_Taste_autenticazione.limiter_config import limiter



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
        # Chiamata al servizio di registrazione del paziente
        return PazienteService.register_paziente(s_paziente)
