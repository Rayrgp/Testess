import pyautogui as pag
import time

# Configurações de segurança
pag.FAILSAFE = True
pag.PAUSE = 0.5

def encontrar_coordenadas():
    """Script para encontrar coordenadas do mouse na tela."""
    print("=== ENCONTRADOR DE COORDENADAS ===")
    print("Instruções:")
    print("1. Mova o mouse para a posição da conta do Google")
    print("2. Pressione Ctrl+C para capturar as coordenadas")
    print("3. Mova o mouse para o canto superior esquerdo para sair")
    print()
    
    try:
        while True:
            x, y = pag.position()
            rgb = pag.screenshot().getpixel((x, y))
            print(f"Posição: ({x}, {y}) | Cor RGB: {rgb}", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        x, y = pag.position()
        print(f"\n\nCoordenadas capturadas: ({x}, {y})")
        print("Use essas coordenadas no seu script principal!")
        print("Exemplo: clicar_na_conta_google(x={}, y={})".format(x, y))

def encontrar_multiplas_coordenadas():
    """Script para encontrar múltiplas coordenadas."""
    print("=== ENCONTRADOR DE MÚLTIPLAS COORDENADAS ===")
    print("Instruções:")
    print("1. Mova o mouse para cada ponto que você quer clicar")
    print("2. Pressione Enter para capturar cada coordenada")
    print("3. Digite 'fim' quando terminar")
    print()
    
    coordenadas = []
    
    try:
        while True:
            input("Posicione o mouse e pressione Enter (ou digite 'fim' para terminar)...")
            x, y = pag.position()
            coordenadas.append((x, y))
            print(f"Coordenada {len(coordenadas)} capturada: ({x}, {y})")
            
            continuar = input("Continuar? (s/n): ").lower()
            if continuar in ['n', 'não', 'nao', 'fim']:
                break
                
    except KeyboardInterrupt:
        print("\nCaptura interrompida pelo usuário")
    
    if coordenadas:
        print(f"\n=== COORDENADAS CAPTURADAS ===")
        print("Use este código no seu script principal:")
        print()
        print("pontos_para_clicar = [")
        for i, (x, y) in enumerate(coordenadas, 1):
            print(f"    ({x}, {y}),  # Ponto {i}")
        print("]")
        print()
        print("clicar_em_pontos(pontos_para_clicar, tempo_entre_cliques=3)")

def testar_coordenadas(x, y):
    """Testa clicar em coordenadas específicas."""
    print(f"Testando clique em ({x}, {y})...")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    try:
        pag.click(x, y)
        print("Clique realizado!")
    except Exception as e:
        print(f"Erro no clique: {e}")

if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Encontrar coordenadas")
    print("2. Encontrar múltiplas coordenadas")
    print("3. Testar coordenadas específicas")
    
    opcao = input("Digite 1, 2 ou 3: ")
    
    if opcao == "1":
        encontrar_coordenadas()
    elif opcao == "2":
        encontrar_multiplas_coordenadas()
    elif opcao == "3":
        x = int(input("Digite a coordenada X: "))
        y = int(input("Digite a coordenada Y: "))
        testar_coordenadas(x, y)
    else:
        print("Opção inválida!")