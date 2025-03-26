
from F_Taste_autenticazione.kafka.kafka_producer import send_kafka_message
from F_Taste_autenticazione.kafka.kafka_consumer import wait_for_kafka_response




class AdminService:
  
    
    @staticmethod
    def login_admin(id_admin,password):
        message={"id_admin":id_admin,"password":password}
        send_kafka_message("admin.login.request",message)
        response=wait_for_kafka_response(["admin.login.success", "admin.login.failed"])
        return response
    
    #da provare
    @staticmethod
    def register_nutrizionista(s_nutrizionista):
        message = {
        "nome": s_nutrizionista['nome'],
        "cognome": s_nutrizionista['cognome'],
        "password": s_nutrizionista['password'],
        "email": s_nutrizionista['email']
    }
        send_kafka_message("admin.dietitianRegistration.request",message)
        response=wait_for_kafka_response(["admin.dietitianRegistration.success", "admin.dietitianRegistration.failed"])
        return response

  