import os



reset_password = os.environ.get('RESET_PASSWORD', "tOecxGrB3z3yVJAuVlLZGsrkVX1Ah6ECjmh6vH0RiFPdqxu3EC3Ycta7QIpe")
endpoint = "https://f-taste.bcsoft.net/"
secret_key = os.environ.get('SECRET_KEY', b"\xf2\n\xdf\x07#\xd6J/ \x88\xa0\xb4'\x0f\xc7\x15")

admin_id = os.environ.get('ADMIN_ID')
admin_password = os.environ.get('ADMIN_PASSWORD')

def get_key():
    return os.environ.get('ENCRYPTION_KEY', 'Bcsoft!1')
