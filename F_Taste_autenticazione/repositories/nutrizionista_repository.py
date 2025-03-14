from F_Taste_autenticazione.db import get_session
from F_Taste_autenticazione.models.nutrizionista import NutrizionistaModel

class NutrizionistaRepository:

  

    @staticmethod
    def find_by_id(id_nutrizionista, session=None):
        session = session or get_session('dietician')
        return session.query(NutrizionistaModel).filter_by(id_nutrizionista=id_nutrizionista).first()

    @staticmethod
    def find_by_email(email, session=None):
        session = session or get_session('dietician')
        return session.query(NutrizionistaModel).filter_by(email=email).first()

    @staticmethod
    def add(nutrizionista, session=None):
        session = session or get_session('dietician')
        session.add(nutrizionista)
        session.commit()

    @staticmethod
    def delete(nutrizionista, session=None):
        session = session or get_session('dietician')
        session.delete(nutrizionista)
        session.commit()
