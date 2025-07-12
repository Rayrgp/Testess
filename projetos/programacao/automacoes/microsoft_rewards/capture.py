import pyautogui as pag
import time
import os

# Configurações de segurança
pag.FAILSAFE = True
pag.PAUSE = 0.5

def capturar_imagem():
    """Captura uma região da tela para usar como referência."""
    print("=== CAPTURADOR DE IMAGEM ===")
    print("Instruções:")
    print("1. Posicione o mouse no canto superior esquerdo da área que deseja capturar")
    print("2. Pressione Enter")
    print("3. Posicione o mouse no canto inferior direito da área")
    print("4. Pressione Enter novamente")
    print("5. Digite o nome do arquivo (ex: alvo1.png)")
    print()
    
    try:
        input("Posicione o mouse no canto superior esquerdo e pressione Enter...")
        x1, y1 = pag.position()
        print(f"Ponto 1: ({x1}, {y1})")
        
        input("Posicione o mouse no canto inferior direito e pressione Enter...")
        x2, y2 = pag.position()
        print(f"Ponto 2: ({x2}, {y2})")
        
        # Calcular dimensões
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        left = min(x1, x2)
        top = min(y1, y2)
        
        print(f"Região: {width}x{height} pixels")
        
        nome_arquivo = input("Digite o nome do arquivo (ex: alvo1.png): ")
        if not nome_arquivo.endswith('.png'):
            nome_arquivo += '.png'
        
        # Capturar a região
        screenshot = pag.screenshot(region=(left, top, width, height))
        screenshot.save(nome_arquivo)
        
        print(f"Imagem salva como: {nome_arquivo}")
        print(f"Use esta imagem no script principal: scroll(alvo='{nome_arquivo}')")
        
    except Exception as e:
        print(f"Erro ao capturar imagem: {e}")

def visualizar_tela():
    """Mostra informações sobre a tela atual."""
    print("=== INFORMAÇÕES DA TELA ===")
    width, height = pag.size()
    print(f"Resolução da tela: {width}x{height}")
    
    x, y = pag.position()
    print(f"Posição atual do mouse: ({x}, {y})")
    
    # Capturar cor do pixel atual
    try:
        rgb = pag.screenshot().getpixel((x, y))
        print(f"Cor do pixel atual: RGB{rgb}")
    except Exception as e:
        print(f"Erro ao obter cor: {e}")

def testar_reconhecimento(arquivo):
    """Testa o reconhecimento de uma imagem."""
    if not os.path.exists(arquivo):
        print(f"Arquivo '{arquivo}' não encontrado!")
        return
    
    print(f"Testando reconhecimento de: {arquivo}")
    
    try:
        print("Procurando elemento na tela...")
        pos = pag.locateOnScreen(arquivo, confidence=0.8)
        if pos:
            print(f"Elemento encontrado em: {pos}")
            pag.moveTo(pos)
            print("Mouse movido para o elemento!")
        else:
            print("Elemento não encontrado na tela atual")
    except Exception as e:
        print(f"Erro ao testar reconhecimento: {e}")
        import traceback
        print("Detalhes completos do erro:")
        print(traceback.format_exc())

if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Capturar imagem de referência")
    print("2. Visualizar informações da tela")
    print("3. Testar reconhecimento de imagem")
    
    opcao = input("Digite 1, 2 ou 3: ")
    
    if opcao == "1":
        capturar_imagem()
    elif opcao == "2":
        visualizar_tela()
    elif opcao == "3":
        arquivo = input("Digite o nome do arquivo de imagem: ")
        testar_reconhecimento(arquivo)
    else:
        print("Opção inválida!") 