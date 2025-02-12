# from flaskr import db
from flaskr.ma import ma
from flaskr.models.richiesta_aggiunta_paziente import RichiestaAggiuntaPazienteModel
from marshmallow import fields
from flaskr.schemas.nutrizionista import NutrizionistaSchema

class RichiestaAggiuntaPazienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RichiestaAggiuntaPazienteModel
        load_instance = True
        # sqla_session = db.session
        include_relationship = True
        

    nutrizionista = fields.Nested(NutrizionistaSchema, only=['id_nutrizionista', 'nome', 'cognome'], dump_only=True)