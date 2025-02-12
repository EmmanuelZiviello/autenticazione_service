from flaskr.db import get_session
from flaskr.models.paziente import PazienteModel
from flaskr.models.nutrizionista import NutrizionistaModel
from sqlalchemy.exc import SQLAlchemyError

class PazienteRepository:

    @staticmethod
    def find_by_email(email, session=None):
        session = session or get_session('patient')
        return session.query(PazienteModel).filter_by(email=email).first()

    @staticmethod
    def find_by_id(id_paziente, session=None):
        session = session or get_session('patient')
        return session.query(PazienteModel).filter_by(id_paziente=id_paziente).first()

    @staticmethod
    def add(paziente, session=None):
        session = session or get_session('patient')
        session.add(paziente)
        session.commit()



    @staticmethod
    def aggiorna_nutrizionista(paziente, id_nutrizionista, nutrizionista,session=None):
        session=session or get_session('patient')
        paziente.fk_nutrizionista = id_nutrizionista
        paziente.nutrizionista =nutrizionista
        session.add(paziente)
        return paziente
    

    @staticmethod
    def revoca_nutrizionista(paziente, session=None):
        session=session or get_session('patient')
        paziente.fk_nutrizionista =None
        paziente.nutrizionista =None
        session.add(paziente)
        return paziente
    
   
