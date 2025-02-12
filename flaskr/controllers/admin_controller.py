
from flask import request
from flask_restx import Resource, fields
from flaskr.namespaces import admin_ns
from flaskr.limiter_config import limiter
from flaskr.services.admin_service import AdminService
from flaskr.schemas.nutrizionista import NutrizionistaSchema
from flaskr.utils.jwt_custom_decorators import admin_required

login_admin = admin_ns.model('admin login', {
    'password': fields.String('password of the admin'),
    'id_admin': fields.String('id of the admin')
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
    @admin_ns.expect(nutrizionista_schema)
    @admin_ns.doc('registra nutrizionista')
    def post(self):
        s_nutrizionista = request.get_json()        
        # Chiamata al servizio di registrazione del nutrizionista
        return AdminService.register_nutrizionista(s_nutrizionista)
