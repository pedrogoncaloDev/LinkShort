from slowapi import Limiter
from slowapi.util import get_remote_address

# Em memória (um único processo/container, sem Redis) — suficiente pro
# tamanho atual do projeto. Compartilhado entre main.py (setup do app) e
# routes.py (decorator @limiter.limit nos endpoints).
limiter = Limiter(key_func=get_remote_address)
