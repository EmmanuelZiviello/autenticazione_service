from F_Taste_autenticazione.repositories.admin_repository import AdminRepository
from F_Taste_autenticazione.utils.jwt_token_factory import JWTTokenFactory
from F_Taste_autenticazione.db import get_session
from F_Taste_autenticazione.repositories.nutrizionista_repository import NutrizionistaRepository
from F_Taste_autenticazione.schemas.nutrizionista import NutrizionistaSchema
from F_Taste_autenticazione.utils.hashing_password import hash_pwd



jwt_factory = JWTTokenFactory()

nutrizionista_schema = NutrizionistaSchema()


class AdminService:
    @staticmethod
    def login_admin(id_admin, password):
        stored_id, stored_password = AdminRepository.get_admin_credentials()
        if id_admin == stored_id and password == stored_password:
            return {
                "esito": "successo",
                "access_token": jwt_factory.create_access_token(id_admin, 'admin'),
                "refresh_token": jwt_factory.create_access_token(id_admin, 'admin')
            }, 200
        return {"esito": "credenziali errate"}, 401
    
    @staticmethod
    def register_nutrizionista(s_nutrizionista):
        session = get_session('admin')
        # Validazione dei dati di input
        validation_errors = nutrizionista_schema.validate(s_nutrizionista)
        if validation_errors:
            session.close()
            return validation_errors, 400

        # Verifica se l'email è già utilizzata
        nutrizionista= NutrizionistaRepository.find_by_email(s_nutrizionista['email'], session)
        if nutrizionista is not None:
            session.close()
            return {'message': 'email già utilizzata'}, 409

        # Carica il nutrizionista nel modello
        nutrizionista = nutrizionista_schema.load(s_nutrizionista,session=session)
        nutrizionista.password = hash_pwd(s_nutrizionista['password'])
        # Aggiungi il nutrizionista al database
        NutrizionistaRepository.add(nutrizionista, session)
        session.close()
        return {'message': 'registrazione avvenuta con successo'}, 201