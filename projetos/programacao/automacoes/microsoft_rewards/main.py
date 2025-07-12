import pyautogui as pag
import time
import subprocess
import random
import string
import os
import webbrowser

# Configurações de segurança do PyAutoGUI
pag.FAILSAFE = True  # Move o mouse para o canto superior esquerdo para parar
pag.PAUSE = 0.5  # Pausa entre comandos

def palavra_aleatoria(tamanho=8):
    """Gera uma palavra aleatória de letras minúsculas."""
    return ''.join(random.choices(string.ascii_lowercase, k=tamanho))

def abrir_chrome(url="https://www.google.com",speed=False):
    """Abre o navegador no site desejado e clica em uma posição específica da tela."""
    webbrowser.open(url)
    if not speed:
        time.sleep(8)
      # Aguarda o navegador abrir
    pag.moveTo(100,200)


def clicar(x,y):
    time.sleep(0.3)
    try:
        # Verifica se as coordenadas estão dentro da tela
        screen_width, screen_height = pag.size()
        if x > screen_width or y > screen_height:
            print(f"ERRO: Coordenadas ({x}, {y}) estão fora da tela!")
            print(f"Tamanho da tela: {screen_width}x{screen_height}")
            return False
        
        pag.click(x, y)
        time.sleep(2)
        print("Clique realizado com sucesso!")
        time.sleep(0.2)
        return True
    except Exception as e:
        print(f"Erro ao clicar: {e}")
        return False
    
    
def clicar_na_conta_google(x=551, y=505):
    '''if not alvo_tela("image.png"):
        """Clica na posição do perfil do Google."""
        try:
            print(f"Clicando na conta do Google em ({x}, {y})...")
            # Verifica se as coordenadas estão dentro da tela
            screen_width, screen_height = pag.size()
            if x > screen_width or y > screen_height:
                print(f"ERRO: Coordenadas ({x}, {y}) estão fora da tela!")
                print(f"Tamanho da tela: {screen_width}x{screen_height}")
                return False
            
            pag.click(x, y)
            time.sleep(2)
            print("Clique realizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao clicar na conta do Google: {e}")
            return False
    else:
        pass'''
    return True

def pesquisar_no_chrome(pesquisa,):
    """Realiza uma pesquisa no Chrome."""
    try:
        print(f"Realizando pesquisa: {pesquisa}")
        pag.hotkey('ctrl', 'l')
        time.sleep(1)
        pag.typewrite(f"{pesquisa}", interval=0.05)
        time.sleep(0.5)
        pag.press('enter')
        time.sleep(5)
        print("Pesquisa realizada com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar pesquisa: {e}")
        raise

def pesquisas_aleatorias_pc(repeticoes=30, tempo_espera=4, x=551, y=505):
    """Realiza pesquisas aleatórias no Chrome."""
    try:
        abrir_chrome()
        '''if not clicar_na_conta_google(x, y):
            print("Falha ao clicar na conta do Google. Abortando...")
            return'''
        
        for i in range(repeticoes):
            pesquisa = palavra_aleatoria(random.randint(5, 12))
            print(f"Pesquisando: {pesquisa} ({i+1}/{repeticoes})")
            pesquisar_no_chrome(pesquisa)
            time.sleep(tempo_espera)
    except Exception as e:
        print(f"Erro durante pesquisas aleatórias: {e}")
        raise
    time.sleep(3)


def scroll(alvo):    
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(alvo):
            print(f"ERRO: Arquivo '{alvo}' não encontrado!")
            print(f"Diretório atual: {os.getcwd()}")
            print(f"Arquivos na pasta: {os.listdir('.')}")
            return False
        
        print(f"Procurando elemento na imagem: {alvo}")
        
        # Aguardar um pouco para a página carregar completamente
        print("Aguardando página carregar...")
        time.sleep(3)
        
        # Tente encontrar o elemento até aparecer
        for tentativa in range(20):
            print(f"Tentativa {tentativa + 1}/20...")
            try:
                # Tentar com diferentes níveis de confiança
                for confianca in [0.9, 0.8]:
                    try:
                        pos = pag.locateOnScreen(alvo, confidence=confianca)
                        if pos:
                            print(f"Elemento encontrado em: {pos} (confiança: {confianca})")
                            pag.moveTo(pos)
                            return True
                    except Exception as e:
                        print(f"Erro com confiança {confianca}: {e}")
                        continue
                
                print("Elemento não encontrado nesta tentativa")
            except Exception as e:
                print(f"Erro ao procurar elemento na tentativa {tentativa + 1}: {e}")
                import traceback
                print(traceback.format_exc())
            
            # Scroll apenas se não encontrou o elemento
            try:
                pag.scroll(-300)  # Desce a página
                time.sleep(0.5)  # Aumentado o tempo de espera
            except Exception as e:
                print(f"Erro ao fazer scroll: {e}")
        
        print("Elemento não encontrado após 20 tentativas")
        return False
    except Exception as e:
        print(f"Erro geral durante scroll: {e}")
        import traceback
        print("Detalhes do erro:")
        print(traceback.format_exc())
        return False
def alvo_tela(alvo):

    try:
        # Verificar se o arquivo existe
        if not os.path.exists(alvo):
            print(f"ERRO: Arquivo '{alvo}' não encontrado!")
            print(f"Diretório atual: {os.getcwd()}")
            print(f"Arquivos na pasta: {os.listdir('.')}")
            return False
        
        print(f"Procurando elemento na imagem: {alvo}")
        
        # Aguardar um pouco para a página carregar completamente
        print("Aguardando página carregar...")
        time.sleep(3)
        
        # Tente encontrar o elemento até aparecer
        for tentativa in range(10):
            print(f"Tentativa {tentativa + 1}/10...")
            try:
                # Tentar com diferentes níveis de confiança
                for confianca in [0.9, 0.8, 0.7]:
                    try:
                        pos = pag.locateOnScreen(alvo, confidence=confianca)
                        if pos:
                            print(f"Elemento encontrado em: {pos} (confiança: {confianca})")
                            pag.moveTo(pos)
                            return True
                    except Exception as e:
                        print(f"Erro com confiança {confianca}: {e}")
                        continue
                
                print("Elemento não encontrado nesta tentativa")
            except Exception as e:
                print(f"Erro ao procurar elemento na tentativa {tentativa + 1}: {e}")
                import traceback
                print(traceback.format_exc())
        print("Elemento não encontrado.")
        return False
    except Exception as e:
        print(f"Erro geral durante busca do alvo: {e}")
        import traceback
        print("Detalhes do erro:")
        print(traceback.format_exc())
        return False

def scroll_simples(quantidade=1):
    """Desce a página um número específico de vezes."""
    try:
        print(f"Descer página {quantidade} vez(es)...")
        
        for i in range(quantidade):
            print(f"Scroll {i+1}/{quantidade}")
            pag.scroll(-300)  # Desce a página
            time.sleep(0.5)  # Aguarda 1 segundo entre cada scroll
        
        print(f"Scroll concluído: {quantidade} vez(es)")
        return True
    except Exception as e:
        print(f"Erro ao fazer scroll simples: {e}")
        return False

def fechar_chrome():
    """Fecha o Chrome de forma mais robusta."""
    try:
        print("Fechando o Chrome...")
        time.sleep(2)
        
        # Método 1: Tentar fechar com Alt+F4
        try:
            pag.hotkey('alt', 'f4')
            time.sleep(1)
            print("Chrome fechado com Alt+F4")
            return True
        except Exception as e:
            print(f"Erro ao fechar com Alt+F4: {e}")
        
        # Método 2: Tentar clicar no X da janela
        try:
            # Coordenadas do botão X (ajuste conforme sua resolução)
            screen_width, screen_height = pag.size()
            x_button_x = screen_width - 10  # 10 pixels da borda direita
            x_button_y = 10  # 10 pixels do topo
            
            pag.click(x_button_x, x_button_y)
            time.sleep(1)
            print("Chrome fechado clicando no X")
            return True
        except Exception as e:
            print(f"Erro ao clicar no X: {e}")
        
        # Método 3: Usar Ctrl+Shift+Q (fecha todas as abas)
        try:
            pag.hotkey('ctrl', 'shift', 'q')
            time.sleep(1)
            print("Chrome fechado com Ctrl+Shift+Q")
            return True
        except Exception as e:
            print(f"Erro ao fechar com Ctrl+Shift+Q: {e}")
        
        print("Não foi possível fechar o Chrome automaticamente")
        return False
        
    except Exception as e:
        print(f"Erro geral ao fechar Chrome: {e}")
        return False

def missoes(x=551, y=505):
    """Acessa a página de missões do Bing Rewards."""
    try:
        print("Iniciando função de missões...")
        
        abrir_chrome(url="https://rewards.bing.com/")

        
        '''if not clicar_na_conta_google(x, y):
            print("Falha ao clicar na conta do Google. Abortando missões...")
            return'''
        
        alvo_path = os.path.join(os.getcwd(), "alvo1.png")
        if not scroll(alvo=alvo_path):
            print("Falha ao encontrar elemento na página de missões")
        clicar(404,655)
        pag.hotkey('ctrl', '1')
        clicar(873,637)
        pag.hotkey('ctrl', '1')
        clicar(1192,642)
        pag.hotkey('ctrl', '1')

        scroll_simples(4)
        time.sleep(1)

        clicar(404,655)
        pag.hotkey('ctrl', '1')
        clicar(873,637)
        pag.hotkey('ctrl', '1')
        clicar(1192,642)
        pag.hotkey('ctrl', '1')

        scroll_simples(2)
        time.sleep(1)

        clicar(224,638)
        pag.hotkey('ctrl', '1')
        clicar(529,655)
        pag.hotkey('ctrl', '1')
        clicar(873,637)
        pag.hotkey('ctrl', '1')
        clicar(1192,642)
        pag.hotkey('ctrl', '1')

        scroll_simples(3)
        time.sleep(1)

        clicar(224,638)
        pag.hotkey('ctrl', '1')
        clicar(529,655)
        pag.hotkey('ctrl', '1')
        clicar(873,637)
        pag.hotkey('ctrl', '1')
        clicar(1192,642)
        pag.hotkey('ctrl', '1')
        
        time.sleep(3)
        

    except Exception as e:
        print(f"Erro durante execução das missões: {e}")
        raise

def start_inicial():
    abrir_chrome(url="https://rewards.bing.com/",speed=True)
    fechar_chrome()

if __name__ == "__main__":
    try:
        print("=== INICIANDO AUTOMAÇÃO ===")
        print("DICA: Mova o mouse para o canto superior esquerdo para parar a automação")
        start_inicial()
        
        missoes()
        print("Missões concluídas com sucesso!")
        fechar_chrome()

        pesquisas_aleatorias_pc()
        print("Pesquisas concluídas com sucesso!") 
        fechar_chrome()

        

        

    except KeyboardInterrupt:
        print("\nAutomação interrompida pelo usuário")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        print("Verifique se:")
        print("1. O Chrome está instalado no caminho padrão")
        print("2. As coordenadas da conta do Google estão corretas")
        print("3. O arquivo alvo1.png existe na pasta")
    finally:
        print("=== FIM DA AUTOMAÇÃO ===")
