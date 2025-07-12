import tkinter as tk
from tkinter import ttk, messagebox
from pynput.keyboard import Controller, Key
import keyboard
import time
import random
import threading

class DigitadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Digitador Automático")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Centralizar a janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
        
        # Variáveis
        self.keyboard_controller = Controller()
        self.digitando = False
        self.thread_digitacao = None
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Digitador Automático", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Label e campo para o texto
        ttk.Label(main_frame, text="Texto para digitar:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text widget com scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 15))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.texto_widget = tk.Text(text_frame, height=8, width=50, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.texto_widget.yview)
        self.texto_widget.configure(yscrollcommand=scrollbar.set)
        
        self.texto_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Frame para configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        config_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        config_frame.columnconfigure(1, weight=1)
        
        # Velocidade de digitação
        ttk.Label(config_frame, text="Velocidade (segundos):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.velocidade_var = tk.StringVar(value="0.2")
        velocidade_entry = ttk.Entry(config_frame, textvariable=self.velocidade_var, width=10)
        velocidade_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Checkbox para velocidade aleatória
        self.velocidade_aleatoria_var = tk.BooleanVar()
        ttk.Checkbutton(config_frame, text="Velocidade aleatória", 
                       variable=self.velocidade_aleatoria_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Delay antes de começar
        ttk.Label(config_frame, text="Delay inicial (segundos):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.delay_var = tk.StringVar(value="5")
        delay_entry = ttk.Entry(config_frame, textvariable=self.delay_var, width=10)
        delay_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Frame para botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Botões
        self.btn_iniciar = ttk.Button(botoes_frame, text="Iniciar Digitação", command=self.iniciar_digitacao)
        self.btn_iniciar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_parar = ttk.Button(botoes_frame, text="Parar", command=self.parar_digitacao, state=tk.DISABLED)
        self.btn_parar.pack(side=tk.LEFT)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para digitar")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10))
        status_label.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        
        # Instruções
        instrucoes = ttk.Label(main_frame, text="Dica: Pressione 'ESC' para parar a digitação a qualquer momento", 
                              font=("Arial", 9), foreground="gray")
        instrucoes.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # Configurar expansão do grid
        main_frame.rowconfigure(2, weight=1)
        
    def obter_velocidade(self):
        if self.velocidade_aleatoria_var.get():
            n = random.randint(0, 4)
            if n == 0 or n == 2:
                return 0.2
            elif n == 1:
                return 0.1
            elif n == 3:
                return 0.15
            else:
                return 0.25
        else:
            try:
                return float(self.velocidade_var.get())
            except ValueError:
                return 0.2
    
    def digitar_texto_com_velocidade(self, texto, velocidade):
        for char in texto:
            if not self.digitando:
                break
                
            if char == '\n':
                self.keyboard_controller.press(Key.enter)
                self.keyboard_controller.release(Key.enter)
            else:
                self.keyboard_controller.press(char)
                self.keyboard_controller.release(char)
            
            time.sleep(velocidade)
    
    def thread_digitacao_func(self):
        try:
            texto = self.texto_widget.get("1.0", tk.END).strip()
            if not texto:
                self.root.after(0, lambda: messagebox.showwarning("Aviso", "Por favor, insira um texto para digitar."))
                return
            
            # Delay inicial
            delay = float(self.delay_var.get())
            self.root.after(0, lambda: self.status_var.set(f"Aguardando {delay} segundos..."))
            time.sleep(delay)
            
            if not self.digitando:
                return
            
            self.root.after(0, lambda: self.status_var.set("Digitando..."))
            
            # Iniciar digitação
            self.digitar_texto_com_velocidade(texto, self.obter_velocidade())
            
            if self.digitando:
                self.root.after(0, lambda: self.status_var.set("Digitação concluída!"))
                self.root.after(0, self.parar_digitacao)
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante a digitação: {str(e)}"))
            self.root.after(0, self.parar_digitacao)
    
    def iniciar_digitacao(self):
        if self.digitando:
            return
            
        self.digitando = True
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)
        self.status_var.set("Preparando...")
        
        # Iniciar thread de digitação
        self.thread_digitacao = threading.Thread(target=self.thread_digitacao_func, daemon=True)
        self.thread_digitacao.start()
    
    def parar_digitacao(self):
        self.digitando = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.status_var.set("Pronto para digitar")
    
    def on_closing(self):
        if self.digitando:
            if messagebox.askokcancel("Sair", "A digitação está em andamento. Deseja realmente sair?"):
                self.digitando = False
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = DigitadorGUI(root)
    
    # Configurar fechamento da janela
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Focar na janela
    root.focus_force()
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()

