import random
from string import ascii_uppercase as uppercase_letters
from string import ascii_lowercase as lowercase_letters
from string import digits as numbers


class PasswordGenerator():

    def __init__(self):
        # Simboli da dover inserire nella password generata casualmente
        self.symbols = '!$%&?@_'
        # Combinazione di tutti i caratteri
        self.all_characters = uppercase_letters + lowercase_letters + numbers + self.symbols
        # Dizionario dei valori predefiniti
        self.predefined_characters = {
                                        "1": [ "!", "#", "$", "%", "&","<",">","?","@"],
                                        "2": ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z" ],
                                        "3": ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
                                        "4": ["0","1","2","3","4","5","6","7","8","9"]
                                    }


    # Funzione che quando richiamata genera una password inserendo caratteri alfanumerici maiuscoli e minuscoli
    def generatePassword(self):

        # Definizione di una pasword vuota
        password = ""
        # Ordine iniziale dei blocchi
        order = ["1","2","3","4"]
        # Ordine rimescolato casualmente
        random.shuffle(order)
        
        # Generiamo i 4 blocchi della password, andando di volta in volta a selezionare il simbolo obbligatorio
        # dalla lista di caratteri predefiniti, scelta tramite la sequenza pocanzi definita
        for i in range(4):
            current_required_characters = self.predefined_characters[order[i]]
            current_block = self.generateBlock(current_required_characters)
            password = password + current_block
        
        # Ritorniamo infine la password generata
        return password



    def generateBlock(self, required_characters):

        # Questa flag indica se il carattere obbligatorio è stato inserito
        required_char_inserted = False
        # Definiamo il blocco della password vuoto
        block = ""

        # Andiamo a generare i caratteri del blocco
        for i in range(3):

            # Se siamo all'interimento
            if i == 2 and required_char_inserted is False:
                # Viene aggiunto il un carattere obbligatorio e si esce dalla funzione
                # con il ritorno del blocco corrente
                block = block + random.choice(required_characters)
                return block
            
            # Altrimenti viene scelto se inserire un carattere causale oppure uno obbligatorio
            else:
                choice = random.randint(0,1)
                # Col caso del carattere richiesto viene impostata anche la flag a True
                if choice == 0:
                    block = block + random.choice(required_characters)
                    required_char_inserted = True
                else:
                    block = block + random.choice(self.all_characters)

        # Alla fine del ciclo for, se non ha effettuato un ritorno da solo
        # Ritorniamo il blocco di 3 caratteri così creato
        return block
    

    # Qesto metodo è utile per controllare che una password sia sicura
    @classmethod
    def isAStrongPassword(self, password):

        has_uppercase = any(char in uppercase_letters for char in password)
        has_lowercase = any(char in lowercase_letters for char in password)
        has_number = any(char in numbers for char in password)
        has_symbols = any(char in "!$%&?@_" for char in password )
        is_long = True if len(password) >= 8 else False


        return has_uppercase and has_lowercase and has_symbols and has_number and is_long

# # Test
# def haDuplicati(lista):
#     # Creiamo un set per tenere traccia degli elementi unici
#     elementi_unici = set()
    
#     for elemento in lista:
#         # Se l'elemento è già presente nel set, allora abbiamo trovato un duplicato
#         if elemento in elementi_unici:
#             return True
#         # Altrimenti, aggiungiamo l'elemento al set
#         elementi_unici.add(elemento)
    
#     # Se abbiamo esaminato tutti gli elementi e non abbiamo trovato duplicati, restituiamo False
#     return False


# def test():
#     passwordGenerator = PasswordGenerator()
#     lista = []
#     for i in range(10000):
#         lista.append(passwordGenerator.generatePassword())
#     print(lista)
#     if haDuplicati(lista):
#         print("Sono stati generati duplicati")
#     else: 
#         print("Non sono stati generati duplicati")




# if __name__ == '__main__':
    
#     test()


