from F_Taste_autenticazione.utils.hashing_password import check_pwd
from F_Taste_autenticazione.utils.jwt_token_factory import JWTTokenFactory
from F_Taste_autenticazione.utils.password_generator import PasswordGenerator
from F_Taste_autenticazione.utils.id_generation import genera_id_valido
from F_Taste_autenticazione.utils.hashing_password import hash_pwd
#import di kafka
from F_Taste_autenticazione.kafka.kafka_producer import send_kafka_message
from F_Taste_autenticazione.kafka.kafka_consumer import wait_for_kafka_response
######

jwt_factory = JWTTokenFactory()



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
    
    @staticmethod
    def login_nutrizionista(email_nutrizionista,password):
        message={"email":email_nutrizionista,"password":password}
        send_kafka_message("dietitian.login.request",message)
        response=wait_for_kafka_response(["dietitian.login.success", "dietitian.login.failed"])
        return response

    #da fare
    @staticmethod
    def register_paziente(s_paziente,nutrizionista_email):
        paziente_email=s_paziente['email']
        if not paziente_email:  # Controllo valore vuoto o assente
            return {"message": "email paziente richiesta"}, 400  # HTTP 400 Bad Request
        message={"paziente_email":paziente_email,"nutrizionista_email":nutrizionista_email}
        send_kafka_message("dietitian.registrationPatientFromDietitian.request",message)
        response=wait_for_kafka_response(["dietitian.registrationPatientFromDietitian.success", "dietitian.registrationPatientFromDietitian.failed"])
        return response

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