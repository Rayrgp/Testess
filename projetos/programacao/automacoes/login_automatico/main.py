import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import subprocess
import webbrowser

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
        self.title('Abrir Sites')
        self.configure(bg=BG_COLOR)
        self.geometry('520x480')
        self.minsize(420, 350)
        self.sites = []
        self.json_path = 'sites.json'
        self.create_widgets()
        self.carregar_sites()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', background=BTN_COLOR, foreground=FG_COLOR, font=FONT, borderwidth=0, focusthickness=3, focuscolor=BTN_COLOR, relief='flat')
        style.map('TButton', background=[('active', BTN_HOVER)], relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        style.configure('TCheckbutton', background=CHECK_BG, foreground=FG_COLOR, font=FONT)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=FONT)
        style.configure('TEntry', fieldbackground=ENTRY_BG, background=ENTRY_BG, foreground=FG_COLOR, borderwidth=0)
        style.configure('Vertical.TScrollbar', background=BG_COLOR, troughcolor=BG_COLOR, bordercolor=BG_COLOR, arrowcolor=FG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Título
        title_frame = tk.Frame(self, bg=BG_COLOR)
        title_frame.grid(row=0, column=0, pady=(18, 5), sticky='ew')
        title_frame.grid_columnconfigure(0, weight=1)
        lbl_icon = tk.Label(title_frame, text='🔗', bg=BG_COLOR, fg=BTN_COLOR, font=('Segoe UI Emoji', 18))
        lbl_icon.grid(row=0, column=0, sticky='w', padx=(10, 0))
        lbl_titulo = tk.Label(title_frame, text='Abrir Sites do JSON', font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
        lbl_titulo.grid(row=0, column=1, sticky='w', padx=(8, 0))

        # Separador
        sep1 = tk.Frame(self, bg=SEPARATOR_COLOR, height=2)
        sep1.grid(row=1, column=0, sticky='ew', padx=0, pady=(0, 5))

        # Label do arquivo selecionado
        lbl_arquivo = ttk.Label(self, text='Arquivo: sites.json')
        lbl_arquivo.grid(row=2, column=0, pady=2, sticky='ew', padx=18)

        # Listbox para mostrar os sites
        frame_list = tk.Frame(self, bg=BG_COLOR)
        frame_list.grid(row=3, column=0, padx=18, pady=8, sticky='nsew')
        frame_list.grid_rowconfigure(0, weight=1)
        frame_list.grid_columnconfigure(0, weight=1)
        self.listbox = tk.Listbox(frame_list, bg=LIST_BG, fg=FG_COLOR, selectbackground=BTN_COLOR, font=FONT, relief='flat', highlightthickness=0, borderwidth=0, selectborderwidth=0, activestyle='none')
        self.listbox.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(frame_list, orient='vertical', command=self.listbox.yview, style='Vertical.TScrollbar')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Separador
        sep2 = tk.Frame(self, bg=SEPARATOR_COLOR, height=2)
        sep2.grid(row=4, column=0, sticky='ew', padx=0, pady=(0, 5))

        # Campo de entrada para novo link
        entry_frame = tk.Frame(self, bg=BG_COLOR)
        entry_frame.grid(row=5, column=0, pady=(0, 8), padx=18, sticky='ew')
        entry_frame.grid_columnconfigure(1, weight=1)
        self.entry_link = PlaceholderEntry(entry_frame, placeholder='Digite o link e pressione Enter ou clique em Adicionar', bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, font=FONT, relief='flat', highlightthickness=1, highlightbackground=BTN_COLOR, borderwidth=6)
        self.entry_link.grid(row=0, column=1, sticky='ew', padx=(0, 5), ipady=4)
        self.entry_link.bind('<Return>', lambda e: self.adicionar_link())
        btn_add = ttk.Button(entry_frame, text='Adicionar', command=self.adicionar_link)
        btn_add.grid(row=0, column=2, ipadx=8, ipady=2)

        # Botão para remover selecionados
        btn_remover = ttk.Button(self, text='Remover selecionado(s)', command=self.remover_selecionados)
        btn_remover.grid(row=6, column=0, pady=(0, 8), sticky='ew', padx=120, ipadx=8, ipady=2)

        # Checkbox para modo anônimo
        self.anon_var = tk.BooleanVar(value=True)
        self.chk_anon = ttk.Checkbutton(self, text='Abrir em modo anônimo', variable=self.anon_var)
        self.chk_anon.grid(row=7, column=0, pady=2, sticky='w', padx=22)

        # Botão para abrir sites
        self.btn_abrir = ttk.Button(self, text='Abrir sites', command=self.abrir_sites)
        self.btn_abrir.grid(row=8, column=0, pady=12, sticky='ew', padx=120, ipadx=8, ipady=4)

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

    def salvar_sites(self):
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({'sites': self.sites}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar o arquivo: {e}')

    def abrir_sites(self):
        if not self.sites:
            messagebox.showwarning('Aviso', 'Nenhum site para abrir!')
            return
        anonimo = self.anon_var.get()
        navegador = None
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        if anonimo:
            if os.name == 'nt':
                if os.path.exists(chrome_path):
                    navegador = 'chrome'
                elif os.path.exists(firefox_path):
                    navegador = 'firefox'
            else:
                if os.system('which google-chrome > /dev/null 2>&1') == 0:
                    navegador = 'chrome'
                elif os.system('which firefox > /dev/null 2>&1') == 0:
                    navegador = 'firefox'
            if not navegador:
                messagebox.showwarning('Aviso', 'Navegador compatível não encontrado para modo anônimo. Abrindo normalmente.')
                anonimo = False
        for site in self.sites:
            if anonimo:
                if navegador == 'chrome':
                    subprocess.Popen([chrome_path, '--incognito', site])
                elif navegador == 'firefox':
                    subprocess.Popen([firefox_path, '-private-window', site])
            else:
                webbrowser.open_new_tab(site)
        self.destroy()

if __name__ == '__main__':
    app = DiscordStyleApp()
    app.mainloop()

