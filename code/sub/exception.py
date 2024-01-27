"""

Contient toutes les exceptions utilisées

"""

class ErrIP(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)

    def __str__(self) -> str:
        return "L'adresse IP doit être sous la forme 'x.x.x.x'."
    
class ErrPORT(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)
    
    def __str__(self) -> str:
        return "Le port doit être un entier."