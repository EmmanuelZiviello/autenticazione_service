from F_Taste_autenticazione.kafka.kafka_producer import send_kafka_message
from F_Taste_autenticazione.kafka.kafka_consumer import wait_for_kafka_response






class NutrizionistaService:

   
    @staticmethod
    def login_nutrizionista(email_nutrizionista,password):
        message={"email":email_nutrizionista,"password":password}
        send_kafka_message("dietitian.login.request",message)
        response=wait_for_kafka_response(["dietitian.login.success", "dietitian.login.failed"])
        return response

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
            