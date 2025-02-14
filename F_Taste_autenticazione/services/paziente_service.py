from F_Taste_autenticazione.repositories.paziente_repository import PazienteRepository
from F_Taste_autenticazione.utils.hashing_password import check_pwd
from F_Taste_autenticazione.utils.jwt_token_factory import JWTTokenFactory
from F_Taste_autenticazione.db import get_session
from F_Taste_autenticazione.utils.id_generation import genera_id_valido
from F_Taste_autenticazione.utils.hashing_password import hash_pwd
from F_Taste_autenticazione.schemas.paziente import PazienteSchema

jwt_factory = JWTTokenFactory()

paziente_schema = PazienteSchema(only = ['email', 'password', 'sesso', 'data_nascita'])
paziente_schema_for_load = PazienteSchema(only = ['email', 'password', 'sesso', 'data_nascita', 'id_paziente'])
paziente_schema_post_return = PazienteSchema(only=['id_paziente'])

class PazienteService:

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
        print(output_richiesta)#debug del valore ,
        return output_richiesta
