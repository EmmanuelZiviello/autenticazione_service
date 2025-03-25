from F_Taste_autenticazione.repositories.paziente_repository import PazienteRepository
from F_Taste_autenticazione.utils.hashing_password import check_pwd
from F_Taste_autenticazione.utils.jwt_token_factory import JWTTokenFactory
from F_Taste_autenticazione.db import get_session
from F_Taste_autenticazione.utils.id_generation import genera_id_valido
from F_Taste_autenticazione.utils.hashing_password import hash_pwd
from F_Taste_autenticazione.schemas.paziente import PazienteSchema
from F_Taste_autenticazione.utils.encrypting_id import encrypt_id,decrypt_id
import F_Taste_autenticazione.utils.credentials as credentials
from F_Taste_autenticazione.utils.jwt_functions import ACCESS_EXPIRES
from F_Taste_autenticazione.utils.redis import get_redis_connection

#import di kafka
from F_Taste_autenticazione.kafka.kafka_producer import send_kafka_message
from F_Taste_autenticazione.kafka.kafka_consumer import wait_for_kafka_response
######

from flask_jwt_extended import create_access_token#non sicuro se da inserire qui direttamente

jwt_factory = JWTTokenFactory()

paziente_schema = PazienteSchema(only = ['email', 'password', 'sesso', 'data_nascita'])
paziente_schema_for_load = PazienteSchema(only = ['email', 'password', 'sesso', 'data_nascita', 'id_paziente'])
paziente_schema_post_return = PazienteSchema(only=['id_paziente'])

class PazienteService:

    @staticmethod
    def login_paziente(email_paziente,password):
        message={"email":email_paziente,"password":password}
        send_kafka_message("patient.login.request",message)
        response=wait_for_kafka_response(["patient.login.success", "patient.login.failed"])
        return response
    '''
    @staticmethod
    def login_paziente(email_paziente, password):
        session = get_session('patient')
        paziente = PazienteRepository.find_by_email(email_paziente,session)
        
        if paziente is None:
            session.close()
            return {"esito_login": "Paziente non trovato"}, 401

        if check_pwd(password, paziente.password):
            session.close()
            return {
                "esito_login": "successo",
                "access_token": jwt_factory.create_access_token(paziente.id_paziente, 'patient'),
                "refresh_token": jwt_factory.create_refresh_token(paziente.id_paziente, 'patient'),
                "id_paziente": paziente.id_paziente
            }, 200
        session.close()
        return {"esito_login": "password errata"}, 401
    '''
    '''
    @staticmethod
    def register_paziente(s_paziente):
        session = get_session('patient')

        validation_errors = paziente_schema.validate(s_paziente)

        if validation_errors:
            session.close()
            return validation_errors , 400

        # Verifica se l'email è già presente
        if PazienteRepository.find_by_email(s_paziente['email'], session) is not None:
            session.close()
            return {"esito_registrazione": "email già utilizzata"}, 409

        # Aggiungi ID valido
        s_paziente['id_paziente'] = genera_id_valido()
        
        # Carica il paziente nel modello
        paziente = paziente_schema_for_load.load(s_paziente, session=session)
        paziente.password = hash_pwd(s_paziente['password'])
        
        # Aggiungi il paziente al database
        PazienteRepository.add(paziente, session)
       
        # Invia la email di registrazione
        #try:
         #   send_mail_registrazione_paziente(paziente.id_paziente, paziente.email)
        #except SMTPRecipientsRefused:
         #   session.close()
          #  return {"message": "email non valida"}, 400
        
        output_richiesta= paziente_schema_post_return.dump(paziente), 201
        session.close()
        return output_richiesta
        '''
    
    @staticmethod
    def register_paziente(s_paziente):
        #manda messaggio kafka al servizio paziente per notificare della registrazione
        send_kafka_message("patient.registration.request", s_paziente)
        #aspetta la risposta kafka dal servizio paziente
        response=wait_for_kafka_response(["patient.registration.success", "patient.registration.failed"])
        return response
    '''
    @staticmethod
    def cambio_pw_paziente(id_paziente,json_data):
        session = get_session('patient')
        old_pw=json_data['password']
        new_pw=json_data['new_password']
        paziente = PazienteRepository.find_by_id(id_paziente,session)
        
        if paziente is None:
            session.close()
            return {"message": "Paziente non trovato"}, 401
        if check_pwd(old_pw,paziente.password):
            paziente.password=hash_pwd(new_pw)
            PazienteRepository.add(paziente,session)
            session.close()
            return{"message":"Password aggiornata con successo"},200
        session.close()
        return {"message":"Vecchia Password errata"},400
         '''
    @staticmethod
    def cambio_pw_paziente(id_paziente,json_data):

        message={"password":json_data['password'],"new_password":json_data['new_password'],"id_paziente":id_paziente}
        send_kafka_message("patient.cambiopw.request",message)
        response=wait_for_kafka_response(["patient.cambiopw.success", "patient.cambiopw.failed"])
        return response

    '''
    @staticmethod
    def recupero_pw_paziente(id_paziente):
        session=get_session('patient')
        paziente = PazienteRepository.find_by_id(id_paziente,session)
        
        if paziente is None:
            session.close()
            return {"message": "Paziente non trovato"}, 401
        session.close()
        token=create_access_token(credentials.reset_password,ACCESS_EXPIRES)
        link=credentials.endpoint + "/password_reset?jwt=" + token + "&id=" + encrypt_id(id_paziente)
        #invia email di recupero password
        return {"esito_cambio_pw":"Email di recupero password inviata con successo"},200
        '''
    @staticmethod
    def recupero_pw_paziente(json_data):
        id_paziente=json_data['id_paziente']
        if not id_paziente:  # Controllo valore vuoto o assente
            return {"message": "ID paziente richiesto"}, 400  # HTTP 400 Bad Request
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.recuperopw.request",message)
        response=wait_for_kafka_response(["patient.recuperopw.success", "patient.recuperopw.failed"])
        return response
    
    @staticmethod
    def patch(id_paziente,token,json_data):
        if not id_paziente == credentials.reset_password:
            return {'message': 'not valid'}, 401
        jti = token["jti"]        
        #get_redis_connection().set(jti, "", ex= ACCESS_EXPIRES)
        new_password = json_data['password']
        id = decrypt_id(json_data['id'])
        message={"id_paziente":id,"new_password":new_password}
        send_kafka_message("patient.patch.request",message)
        response=wait_for_kafka_response(["patient.patch.success", "patient.patch.failed"])
        return response
        
        
        
