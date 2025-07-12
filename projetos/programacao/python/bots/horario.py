from datetime import datetime, timezone
import pytz
import os
import time

# Define o fuso horário de Brasília
fuso_brasilia = pytz.timezone('America/Sao_Paulo')

while True:
    os.system("clr")  # ou "cls" no Windows
    agora_utc = datetime.now(timezone.utc)

    # Converte de UTC para horário de Brasília
    agora_brasilia = agora_utc.astimezone(fuso_brasilia)

    print("Hora UTC:", agora_utc.strftime("%H:%M:%S"))
    print("Hora em Brasília:", agora_brasilia.strftime("%H:%M:%S"))

    time.sleep(1)  # Espera 1 segundo para atualizar