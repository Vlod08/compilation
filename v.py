mots_cles = ['EOF', "int", "for", "while", "do", "if", "else", "break", "continue", "return"]
operators = ['+', '-', '*', '/', '%', '!', '&', '<', '<=', '>', '>=', '==', '!=', '&&', '||', '(', ')', '[', ']', '{', '}', ',', ';', '=']

class Token:
    def __init__(self, type_, valeur):
        self.type_ = type_
        self.valeur = valeur

def token(file_path):
    tokens = []
    current_token = None
    last_token = None

    with open(file_path, 'r') as file:
        c_code = file.read()

    current_word = ""
    for char in c_code:
        if char.isalnum() or char == '_': #isidentifier
            current_word += char
        else:
            if current_word:
                if current_word in mots_cles:
                    current_token = Token('MOT_CLE', current_word)
                else:
                    current_token = Token('IDENTIFIER', current_word)
                tokens.append(current_token)
                last_token = current_token
                current_word = ""
            if char in operators:
                current_token = Token('OPERATOR', char)
                tokens.append(current_token)
                last_token = current_token

    if current_word:
        if current_word in mots_cles:
            tokens.append(Token('MOT_CLE', current_word))
        else:
            tokens.append(Token('IDENTIFIER', current_word))

    return tokens, current_token, last_token

tokens, current_token, last_token = token("test.c")

for token in tokens:
    print(f"Type: {token.type_}, Valeur: {token.valeur}")
