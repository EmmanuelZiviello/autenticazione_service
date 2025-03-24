from F_Taste_autenticazione.repositories.nutrizionista_repository import NutrizionistaRepository
from F_Taste_autenticazione.repositories.paziente_repository import PazienteRepository

from F_Taste_autenticazione.utils.hashing_password import check_pwd
from F_Taste_autenticazione.utils.jwt_token_factory import JWTTokenFactory
from F_Taste_autenticazione.schemas.nutrizionista import NutrizionistaSchema
from F_Taste_autenticazione.schemas.paziente import PazienteSchema
from F_Taste_autenticazione.db import get_session
from F_Taste_autenticazione.utils.password_generator import PasswordGenerator
from F_Taste_autenticazione.utils.id_generation import genera_id_valido
from F_Taste_autenticazione.utils.hashing_password import hash_pwd

#import di kafka
from F_Taste_autenticazione.kafka.kafka_producer import send_kafka_message
from F_Taste_autenticazione.kafka.kafka_consumer import wait_for_kafka_response
######

jwt_factory = JWTTokenFactory()
nutrizionista_schema = NutrizionistaSchema(load_instance=False, only=('email', 'password'))
paziente_schema_post = PazienteSchema(partial=['id_paziente', 'fk_nutrizionista', 'data_nascita', 'sesso', 'password'], load_only=['id_paziente', 'password'])


class NutrizionistaService:

    '''
    @staticmethod
    def login_nutrizionista(email, password, json_data):
        session = get_session('dietitian')
        validation_errors = nutrizionista_schema.validate(json_data)
        if validation_errors:
            session.close()
            return validation_errors, 400

        nutrizionista = NutrizionistaRepository.find_by_email(email,session)

        if nutrizionista is None:
            session.close()
            return {"esito_login": "Nutrizionista non trovato"}, 401

        if check_pwd(password, nutrizionista.password):
            session.close()
            return {
                "esito_login": "successo",
                "access_token": jwt_factory.create_access_token(email, 'dietitian'),
                "refresh_token": jwt_factory.create_refresh_token(email, 'dietitian'),
                "id_nutrizionista": nutrizionista.id_nutrizionista
            }, 200

        session.close()
        return {"esito_login": "password errata"}, 401
    '''
    #da provare
    @staticmethod
    def login_nutrizionista(email_nutrizionista,password):
        message={"email":email_nutrizionista,"password":password}
        send_kafka_message("dietitian.login.request",message)
        response=wait_for_kafka_response(["dietitian.login.success", "dietitian.login.failed"])
        return response

    #da fare
    @staticmethod
    def register_paziente(s_paziente,email_nutrizionista):
        email_paziente=s_paziente['email']
        if not email_paziente:  # Controllo valore vuoto o assente
            return {"message": "email paziente richiesta"}, 400  # HTTP 400 Bad Request
        message={"email_nutrizionista":email_nutrizionista}
        send_kafka_message("dietitian.existGet.request",message)
        response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
        if response_nutrizionista.get("status_code") == "200":
            id_nutrizionista=response_nutrizionista.get("id_nutrizionista")
            message={"email_nutrizionista":email_nutrizionista,"email_paziente":email_paziente,"id_nutrizionista":id_nutrizionista}
            send_kafka_message("dietitian.registrationPatientFromDietitian.request",message)
            response_paziente=wait_for_kafka_response(["dietitian.registrationPatientFromDietitian.success", "dietitian.registrationPatientFromDietitian.failed"])
            if response_paziente.get("status_code") == "201":
                return {"esito_registrazione": "successo"}, 201
            elif response_paziente.get("status_code") == "400":
                return {"esito_registrazione":"Dati mancanti"}, 400
            elif response_paziente.get("status_code") == "409":
                return {"esito_registrazione":"Paziente già presente nel db"}
        elif response_nutrizionista.get("status_code") == "400":
            return {"esito_registrazione":"Dati mancanti per il recupero nutrizionista"}, 400
        elif response_nutrizionista.get("status_code") == "404":
            return {"esito_registrazione":"Nutrizionista non presente nel db"}, 404
            
        #message={"paziente_email":paziente_email,"nutrizionista_email":email_nutrizionista}
        #send_kafka_message("dietitian.registrationPatientFromDietitian.request",message)
        #response=wait_for_kafka_response(["dietitian.registrationPatientFromDietitian.success", "dietitian.registrationPatientFromDietitian.failed"])
        #return response

    '''
    @staticmethod
    def register_paziente(s_paziente, nutrizionista_email):
    # Verifica se il nutrizionista esiste nel database
        session = get_session('dietitian')

        if "email" not in s_paziente:
            session.close()
            return {'message' : 'Specifica una email prima di richiedere una registrazione'}, 400
        

        nutrizionista = NutrizionistaRepository.find_by_email(nutrizionista_email, session)
        if  nutrizionista is None:
            session.close()
            return {"message": "Nutrizionista non trovato"}, 401
        
        paziente=PazienteRepository.find_by_email(s_paziente['email'],session)
        if paziente is not None:
            session.close()
            return {"message":"email paziente già in uso"},401
        
        
        # Genera la password e crea il paziente
        passwordGenerator = PasswordGenerator()
        password = passwordGenerator.generatePassword()
        s_paziente['password'] = password
        s_paziente['id_paziente'] = genera_id_valido()
        paziente=paziente_schema_post.load(s_paziente,session=session)
        paziente.password=hash_pwd(password)
        PazienteRepository.add(paziente,session)
        

        paziente=PazienteRepository.aggiorna_nutrizionista(paziente,nutrizionista.id_nutrizionista,nutrizionista,session)
        if paziente is None:
            session.close()
            return {"message":"Errore assegnazione nutrizionista"},400
        session.close()
        return {"esito_registrazione": "successo"}, 201
       
        
        
        # Invia l'email di registrazione
       # try:
        #    send_registration_email(paziente, nutrizionista)
        #except EmailNotFound as e:
         #   raise e

        # Aggiungi paziente e richiesta al database
       # add_paziente_and_request(paziente, nutrizionista, session)
    '''