import random
from ..models import CompInvites


def random_code() -> str:

    characters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    characters += characters.upper()

    code = ''

    for _ in range(random.randint(10, 30)):
        
        code += random.choice(characters)
    print(len(code))
    if CompInvites.objects.filter(code=code).exists():
        random_code()
    
    return code