import string
from sqlalchemy.orm.exc import NoResultFound
import random
from flaskr.db import get_session
from flaskr.repositories.paziente_repository import PazienteRepository

ID_LENGTH = 7

def random_id():
    random_id = ''
    while len(random_id) < ID_LENGTH:
        char = random.choice(string.ascii_uppercase + string.digits)
        if char != '0' and char != 'O':
            random_id += char

    return random_id

def genera_id_valido():
    id_valido = False

    while not id_valido:
        id_paziente = random_id()
        if verifica_disponibilita_id(id_paziente):
            id_valido = True
    return id_paziente

def verifica_disponibilita_id(id):
    session = get_session('patient')
    try:
        result = PazienteRepository.find_by_id(id, session)
        session.close()
        if result is not None:
            return False
        return True
    except NoResultFound as e:
        return True
