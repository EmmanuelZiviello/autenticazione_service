
from F_Taste_autenticazione.utils.encrypting_id import decrypt_id
import F_Taste_autenticazione.utils.credentials as credentials
from F_Taste_autenticazione.utils.jwt_functions import ACCESS_EXPIRES
from F_Taste_autenticazione.utils.redis import get_redis_connection
from F_Taste_autenticazione.kafka.kafka_producer import send_kafka_message
from F_Taste_autenticazione.kafka.kafka_consumer import wait_for_kafka_response


#from flask_jwt_extended import create_access_token#non sicuro se da inserire qui direttamente




class PazienteService:

    @staticmethod
    def login_paziente(email_paziente,password):
        message={"email":email_paziente,"password":password}
        send_kafka_message("patient.login.request",message)
        response=wait_for_kafka_response(["patient.login.success", "patient.login.failed"])
        return response
    
    
    @staticmethod
    def register_paziente(s_paziente):
        #manda messaggio kafka al servizio paziente per notificare della registrazione
        send_kafka_message("patient.registration.request", s_paziente)
        #aspetta la risposta kafka dal servizio paziente
        response=wait_for_kafka_response(["patient.registration.success", "patient.registration.failed"])
        return response
    
    @staticmethod
    def cambio_pw_paziente(id_paziente,json_data):

        message={"password":json_data['password'],"new_password":json_data['new_password'],"id_paziente":id_paziente}
        send_kafka_message("patient.cambiopw.request",message)
        response=wait_for_kafka_response(["patient.cambiopw.success", "patient.cambiopw.failed"])
        return response

    
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
        
        
        
