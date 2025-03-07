from flask import request
from flask_restx import Resource, fields
from F_Taste_autenticazione.namespaces import admin_ns
from F_Taste_autenticazione.limiter_config import limiter
from F_Taste_autenticazione.services.admin_service import AdminService
from F_Taste_autenticazione.schemas.nutrizionista import NutrizionistaSchema
from F_Taste_autenticazione.utils.jwt_custom_decorators import admin_required

login_admin = admin_ns.model('admin login', {
    'password': fields.String('password of the admin'),
    'id_admin': fields.String('id of the admin')
})

nutrizionista_model = admin_ns.model('Nutrizionista', {
    'email': fields.String(description='Email del nutrizionista', required=True),
    'nome': fields.String(description='Nome del nutrizionista', required=True),
    'cognome': fields.String(description='Cognome del nutrizionista', required=True),
    'password': fields.String(description='Password del nutrizionista', required=True),
    'link_informativa': fields.String(description='Link all\'informativa', required=False)
})



nutrizionista_schema = NutrizionistaSchema()

class AdminLogin(Resource):

    @limiter.limit("30/day; 10/hour; 3/minute; 1/second")
    @admin_ns.expect(login_admin)
    @admin_ns.doc('login Admin')
    def post(self):
        data = request.json
        return AdminService.login_admin(data['id_admin'], data['password'])
    

class AdminNutrizionista(Resource):
    @admin_required()
    @admin_ns.expect(nutrizionista_model)
    @admin_ns.doc('registra nutrizionista')
    def post(self):
        s_nutrizionista = request.get_json()        
        # Chiamata al servizio di registrazione del nutrizionista
        return AdminService.register_nutrizionista(s_nutrizionista)
