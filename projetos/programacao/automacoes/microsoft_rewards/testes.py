import pyautogui as pag
import webbrowser
import time

webbrowser.open("https://rewards.bing.com/")
time.sleep(5)  # Aguarda o navegador abrir

# Exemplo: mover o mouse para uma posição e clicar
pag.moveTo(100, 200)
pag.click()