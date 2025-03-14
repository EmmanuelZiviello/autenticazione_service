import os
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_restx import Api, ValidationError as ValidationErr
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound
from smtplib import SMTPException
from flask_cors import CORS
from F_Taste_autenticazione.ma import ma

from F_Taste_autenticazione.namespaces import paziente_ns,admin_ns,nutrizionista_ns
from F_Taste_autenticazione.controllers.admin_controller import AdminLogin,AdminNutrizionista
from F_Taste_autenticazione.controllers.paziente_controller import Paziente,PazienteLogin,PazientePassword
from F_Taste_autenticazione.controllers.nutrizionista_controller import NutrizionistaLogin,NutrizionistaPaziente


from F_Taste_autenticazione.utils.jwt_custom_decorators import NoAuthorizationException



#limiter per gestione login brute force
from F_Taste_autenticazione.limiter_config import limiter, set_limiter_config
#from flaskr.utils.redis import get_redis_connection, init_redis_connection_pool

from logging import getLogger



def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('F_Taste_autenticazione.config.DevelopmentConfig')
   
    #logging.getLogger('flask_cors').level = logging.DEBUG

    
    #Parte di redis
    #if app.config['REDIS_HOST'] is None:
     #   app.config['REDIS_HOST'] = 'localhost'
    #if app.config['REDIS_PORT'] is None:
     #   app.config['REDIS_PORT'] = 6379

    #with app.app_context():
     #   init_redis_connection_pool(app)
        #set_DB_CONFIG()forse da sostituire con create db

    if __name__ != '__main__':
        gunicorn_logger = getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    
    
    # teardown connection pool redis
    #@app.teardown_appcontext
    #def close_redis_connection(exception=None):
     #   redis = get_redis_connection()
      #  if redis is not None:
       #     redis.connection_pool.disconnect()

    #with app.app_context():
        #set_limiter_config()

    # @app.after_request
    # def logAfterRequest(response):
    #     app.logger.info(
    #         "path: %s | method: %s | status: %s ",
    #         request.path,
    #         request.method,
    #         response.status
    #     )
    #     return response

    CORS(app)
    api = Api(app, doc='/doc', title='rest api f-taste documentation')
    jwt = JWTManager(app)

    limiter.init_app(app) #limiter per gestione login brute force

    # controllo se token è in blacklist
   # @jwt.token_in_blocklist_loader
   # def check_if_token_is_revoked(jwt_header, jwt_payload):
    #    if os.environ.get('FLASK_ENV') == "Test":
     #       return False
      #  jti = jwt_payload["jti"]
       # try:
        #    redis_connection = get_redis_connection()
        #except Exception as e:
         #   print(e)
          #  raise e
        #token_in_redis = redis_connection.get(jti)
        #return token_in_redis is not None

    ma.init_app(app)

    #namespaces here
    api.add_namespace(paziente_ns)
    api.add_namespace(nutrizionista_ns)
    api.add_namespace(admin_ns)

    #adding CORS after request
    @app.after_request
    def add_header(response):
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        return response

    #errors handlers here
   # @api.errorhandler(ValidationError)
    #def handle_validations_error(error: ValidationError):
     #   return {'message': 'An error in validation accoured'}, 400

    #@api.errorhandler(ValidationErr)
    #def handle_validations_error(error: ValidationErr):
     #   return error, 400
        
    #@api.errorhandler(NoResultFound)
    #def handle_NoResultFound_error(error: NoResultFound):
     #   return {'message': str(error.args)}, 404

    #@api.errorhandler(EmailNotFound)
    #def handle_EmailNotFound_error(error: EmailNotFound):
     #   return {'message': error.message}, 400

    #@api.errorhandler(SMTPException)
    #def handle_SMTPExceprion_error(error: SMTPException):
     #   return {'message': error.strerror}, 500

    #@api.errorhandler(NoAuthorizationException)
    #def handle_SMTPExceprion_error(error: NoAuthorizationException):
     #   return {'message': error.args}, 403
    

    #nutrizionista resources here
    nutrizionista_ns.add_resource(NutrizionistaPaziente,'/paziente')
    nutrizionista_ns.add_resource(NutrizionistaLogin, '/login')
   
    #paziente resources here
    paziente_ns.add_resource(PazienteLogin, '/login')
    paziente_ns.add_resource(Paziente, '')
    paziente_ns.add_resource(PazientePassword,'/password')

    
    #admin resources here
    admin_ns.add_resource(AdminNutrizionista, '/nutrizionista')
    admin_ns.add_resource(AdminLogin, '/login')
    


    #app.add_url_rule("/password_reset", view_func=TemplatePasswordChangerController.reindirizza, methods=['GET'])
    #app.add_url_rule("/success", view_func=TemplatePasswordChangerController.successo, methods=['GET'])
    #app.add_url_rule("/failure", view_func=TemplatePasswordChangerController.fallimento, methods=['GET'])
    @app.route('/health', methods=['GET'])#è solo per prova
    def health_check():
        return {'message': 'API autenticazione è online'}, 200

    
    return app

