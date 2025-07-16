try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    import json
    import os
    import subprocess
    import webbrowser
    from PIL import Image, ImageTk

except Exception as e:
    print(f"Erro:{e}")

    try:
        import subprocess
        result = subprocess.run("pip install -r requirements.txt",shell=True,capture_output=True,text=True)
        if result.returncode != 0:
            print("Erro ao instalar as dependências:")
            print(result.stderr)
        else:
            print("Dependências instaladas com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar instalar as dependências: {e}")

# Paleta de cores estilo Discord
BG_COLOR = '#2f3136'
FG_COLOR = '#ffffff'
BTN_COLOR = '#5865f2'
BTN_HOVER = '#4752c4'
ENTRY_BG = '#36393f'
LIST_BG = '#23272a'
CHECK_BG = BG_COLOR
SEPARATOR_COLOR = '#202225'
PLACEHOLDER_COLOR = '#888c94'
FONT = ('Segoe UI', 11)
FONT_BOLD = ('Segoe UI', 16, 'bold')

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color=PLACEHOLDER_COLOR, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class DiscordStyleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # Janela sem borda
        self.configure(bg=BG_COLOR)
        self.geometry('540x500')
        self.minsize(480, 400)
        self.sites = []
        self.json_path = 'sites.json'
        self._drag_data = {"x": 0, "y": 0}
        self.create_widgets()
        self.carregar_sites()

    def create_widgets(self):
        # Estilo dos elementos
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', background=BTN_COLOR, foreground=FG_COLOR, font=FONT,
                        borderwidth=0, relief='flat', padding=6)
        style.map('TButton', background=[('active', BTN_HOVER)])
        style.configure('TCheckbutton', background=CHECK_BG, foreground=FG_COLOR, font=FONT)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=FONT)
        style.configure('TEntry', background=ENTRY_BG, foreground=FG_COLOR, font=FONT, relief='flat')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Barra superior
        title_bar = tk.Frame(self, bg=BG_COLOR, height=35)
        title_bar.grid(row=0, column=0, sticky='ew')
        title_bar.grid_columnconfigure(1, weight=1)

        lbl_icon = tk.Label(title_bar, text="🔗", bg=BG_COLOR, fg=BTN_COLOR, font=('Segoe UI Emoji', 16))
        lbl_icon.grid(row=0, column=0, padx=(10, 5))

        lbl_title = tk.Label(title_bar, text="Abrir Sites do JSON", bg=BG_COLOR, fg=FG_COLOR, font=FONT_BOLD)
        lbl_title.grid(row=0, column=1, sticky='w')

        btn_close = tk.Label(title_bar, text="✖", bg=BG_COLOR, fg=FG_COLOR, font=FONT_BOLD, cursor="hand2")
        btn_close.grid(row=0, column=2, sticky='e', padx=10)
        btn_close.bind("<Button-1>", lambda e: self.destroy())

        # Movimentação da janela
        for widget in (title_bar, lbl_title, lbl_icon):
            widget.bind("<Button-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        # Separador horizontal
        separator = tk.Frame(self, bg=SEPARATOR_COLOR, height=2)
        separator.grid(row=1, column=0, sticky='ew', padx=0, pady=(10, 5))

        # Label do arquivo
        lbl_file = ttk.Label(self, text="Arquivo: sites.json")
        lbl_file.grid(row=2, column=0, pady=5, sticky='w', padx=18)

        # Frame da lista de sites
        frame_list = tk.Frame(self, bg=BG_COLOR)
        frame_list.grid(row=3, column=0, padx=18, pady=8, sticky='nsew')
        frame_list.grid_rowconfigure(0, weight=1)
        frame_list.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(frame_list, bg=LIST_BG, fg=FG_COLOR, selectbackground=BTN_COLOR,
                                  font=FONT, relief='flat', highlightthickness=0, activestyle='none')
        self.listbox.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(frame_list, orient='vertical', command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Campo de entrada
        entry_frame = tk.Frame(self, bg=BG_COLOR)
        entry_frame.grid(row=4, column=0, pady=(5, 8), padx=18, sticky='ew')
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_link = PlaceholderEntry(entry_frame, placeholder="Digite o link e pressione Enter",
                                           bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
                                           font=FONT, relief='flat', highlightthickness=1,
                                           highlightbackground=BTN_COLOR, borderwidth=6)
        self.entry_link.grid(row=0, column=0, sticky='ew', ipady=4, padx=(0, 6))
        self.entry_link.bind('<Return>', lambda e: self.adicionar_link())

        btn_add = ttk.Button(entry_frame, text='Adicionar', command=self.adicionar_link)
        btn_add.grid(row=0, column=1, ipadx=6, ipady=2)

        # Botões inferiores
        btns_frame = tk.Frame(self, bg=BG_COLOR)
        btns_frame.grid(row=5, column=0, sticky='ew', padx=18, pady=(6, 4))
        btns_frame.grid_columnconfigure((0, 1), weight=1)

        btn_remover = ttk.Button(btns_frame, text="Remover", command=self.remover_selecionados)
        btn_remover.grid(row=0, column=0, sticky='ew', padx=(0, 4), ipady=4)

        self.btn_abrir = ttk.Button(btns_frame, text="Abrir Sites", command=self.abrir_sites)
        self.btn_abrir.grid(row=0, column=1, sticky='ew', padx=(4, 0), ipady=4)

        # Checkbox Modo Anônimo
        self.anon_var = tk.BooleanVar(value=True)
        self.chk_anon = ttk.Checkbutton(self, text='Abrir em modo anônimo', variable=self.anon_var)
        self.chk_anon.grid(row=6, column=0, pady=(4, 12), sticky='w', padx=22)

    # Função para iniciar o movimento da janela
    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_move(self, event):
        deltax = event.x - self._drag_data["x"]
        deltay = event.y - self._drag_data["y"]
        self.geometry(f'+{self.winfo_x() + deltax}+{self.winfo_y() + deltay}')

    def carregar_sites(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            self.sites = dados.get('sites', [])
            self.listbox.delete(0, tk.END)
            for site in self.sites:
                self.listbox.insert(tk.END, site)
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao carregar o arquivo: {e}')
            self.sites = []
            self.listbox.delete(0, tk.END)

    def adicionar_link(self):
        novo_link = self.entry_link.get().strip()
        if not novo_link or novo_link == self.entry_link.placeholder:
            messagebox.showwarning('Aviso', 'Digite um link para adicionar!')
            return
        if novo_link in self.sites:
            messagebox.showwarning('Aviso', 'Este link já está na lista!')
            return
        self.sites.append(novo_link)
        self.listbox.insert(tk.END, novo_link)
        self.entry_link.delete(0, tk.END)
        self.entry_link.put_placeholder()
        self.salvar_sites()

    def remover_selecionados(self):
        selecionados = list(self.listbox.curselection())
        if not selecionados:
            messagebox.showwarning('Aviso', 'Selecione pelo menos um link para remover!')
            return
        for idx in reversed(selecionados):
            self.listbox.delete(idx)
            del self.sites[idx]
        self.salvar_sites()

    def abrir_sites(self):
        anon = self.anon_var.get()
        chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        for site in self.sites:
            if anon and os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, "--incognito", site])
            else:
                webbrowser.open(site)
        self.destroy()

    def salvar_sites(self):
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({'sites': self.sites}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar o arquivo: {e}')


if __name__ == '__main__':
    app = DiscordStyleApp()
    app.mainloop()

