from random import choice
import re

alfanumerica = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h','H', 'i', 'I', 'j', 'J',
                    'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 
                    'u', 'U' 'v', 'V', 'w', 'W', 'y', 'Y', 'z', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '@', '$', '&', '#', '*', '%', '!']

nova_senha = ''

while True:
    for c in range(0, 15):
        char = choice(alfanumerica)
        nova_senha += char
    
    padrao = re.compile(r'[@#$%^&+=!*]')
    caractere_especial = padrao.search(nova_senha)
    comeca_caractere_especial = padrao.match(nova_senha)
    
    if caractere_especial and not comeca_caractere_especial:
        print(nova_senha)
        break
    else:
        nova_senha = ''
        continue
