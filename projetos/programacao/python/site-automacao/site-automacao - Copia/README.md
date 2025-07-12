# 🚀 App Universal Python

Um aplicativo web moderno criado com Python Flask que funciona perfeitamente tanto no PC quanto no celular!

## ✨ Funcionalidades

- 📱 **Interface Responsiva**: Adapta-se a qualquer tamanho de tela
- ✅ **Gerenciador de Tarefas**: Crie, complete e delete tarefas
- 📝 **Bloco de Notas**: Salve suas ideias e lembretes
- 🧮 **Calculadora**: Calculadora completa com interface moderna
- 🌤️ **Previsão do Tempo**: Dados meteorológicos em tempo real
- 💾 **Persistência de Dados**: Seus dados são salvos localmente

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
2. **Navegue até a pasta do projeto**:
   ```bash
   cd python/automacao
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o aplicativo**:
   ```bash
   python main.py
   ```

## 🌐 Como Acessar

### No PC:
- O navegador abrirá automaticamente em `http://localhost:5000`

### No Celular:
1. Descubra o IP do seu computador na rede:
   - **Windows**: Abra o CMD e digite `ipconfig`
   - **Mac/Linux**: Abra o terminal e digite `ifconfig` ou `ip addr`

2. No celular, acesse: `http://[SEU_IP]:5000`
   - Exemplo: `http://192.168.1.100:5000`

## 📱 Como Usar

### Gerenciador de Tarefas
- Clique em "Nova Tarefa" para adicionar uma tarefa
- Marque a caixa para marcar como concluída
- Clique no ícone de lixeira para deletar

### Bloco de Notas
- Clique em "Nova Nota" para criar uma nota
- Preencha o título e conteúdo
- Clique em "Salvar"

### Calculadora
- Use os botões para fazer cálculos
- Clique em "C" para limpar
- Clique em "=" para ver o resultado

### Previsão do Tempo
- Os dados são carregados automaticamente
- Clique no ícone de atualizar para recarregar

## 🔧 Configuração do Clima (Opcional)

Para obter dados reais do clima:

1. Acesse [OpenWeatherMap](https://openweathermap.org/api)
2. Crie uma conta gratuita
3. Obtenha sua API Key
4. No arquivo `main.py`, substitua `'YOUR_API_KEY'` pela sua chave

## 📁 Estrutura do Projeto

```
python/automacao/
├── main.py              # Aplicativo principal Flask
├── requirements.txt     # Dependências Python
├── README.md           # Este arquivo
├── app_data.json       # Dados salvos (criado automaticamente)
├── templates/
│   └── index.html      # Template HTML principal
└── static/
    ├── styles.css      # Estilos CSS
    └── script.js       # JavaScript do frontend
```

## 🎨 Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Estilização**: CSS Grid, Flexbox, Gradientes
- **Ícones**: Font Awesome
- **Responsividade**: Media Queries

## 🔒 Segurança

- Os dados são salvos localmente no arquivo `app_data.json`
- Não há conexão com bancos de dados externos
- O aplicativo roda apenas na sua rede local

## 🚀 Próximas Funcionalidades

- [ ] Sincronização com nuvem
- [ ] Temas personalizáveis
- [ ] Mais widgets (relógio, cronômetro)
- [ ] Exportação de dados
- [ ] Backup automático

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias e novas funcionalidades!

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

**Desenvolvido com ❤️ usando Python Flask** 