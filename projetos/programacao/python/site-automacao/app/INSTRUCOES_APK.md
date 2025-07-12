# 📱 **Como Criar um APK do App Universal**

## 🎯 **Opções Disponíveis**

### **1. Kivy + Buildozer (Recomendado)**
Criei uma versão móvel do seu app usando **Kivy** que pode ser convertida em APK.

### **2. Alternativas**
- **Flutter** (mais complexo, mas melhor performance)
- **React Native** (JavaScript/TypeScript)
- **Cordova/PhoneGap** (converter web app)

---

## 🚀 **Passo a Passo - Kivy + Buildozer**

### **1. Instalar Dependências**

```bash
# Instalar Python 3.8+ (se não tiver)
# Baixar de: https://www.python.org/downloads/

# Instalar Kivy
pip install kivy

# Instalar Buildozer
pip install buildozer

# No Windows, você também precisará do WSL (Windows Subsystem for Linux)
# ou usar uma máquina virtual Linux
```

### **2. Preparar o Ambiente**

```bash
# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install kivy buildozer
```

### **3. Testar o App Localmente**

```bash
# Testar o app Kivy no computador
python mobile_app.py
```

### **4. Configurar Buildozer**

O arquivo `buildozer.spec` já está configurado. Principais configurações:

```ini
title = App Universal
package.name = appuniversal
package.domain = org.appuniversal
requirements = python3,kivy,urllib3
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
```

### **5. Construir o APK**

```bash
# Inicializar buildozer (já feito)
buildozer init

# Construir APK
buildozer android debug

# Para versão release (assinada)
buildozer android release
```

---

## 🔧 **Solução de Problemas**

### **Erro: "buildozer command not found"**
```bash
pip install --upgrade buildozer
```

### **Erro: "Java not found"**
- Instalar JDK 8 ou 11
- Configurar JAVA_HOME

### **Erro: "Android SDK not found"**
- Buildozer baixa automaticamente
- Pode demorar na primeira vez

### **Erro: "NDK not found"**
- Buildozer baixa automaticamente
- Pode demorar na primeira vez

---

## 📁 **Estrutura do Projeto**

```
automacao/
├── main.py              # App Flask (web)
├── mobile_app.py        # App Kivy (móvel)
├── buildozer.spec       # Configuração APK
├── app_data.json        # Dados salvos
├── templates/           # Templates HTML
├── static/              # CSS/JS
└── INSTRUCOES_APK.md    # Este arquivo
```

---

## 🎨 **Personalização**

### **Ícone do App**
```bash
# Criar pasta data
mkdir data

# Adicionar ícone (192x192px PNG)
# Editar buildozer.spec:
icon.filename = %(source.dir)s/data/icon.png
```

### **Tela de Abertura**
```bash
# Adicionar splash screen
# Editar buildozer.spec:
presplash.filename = %(source.dir)s/data/presplash.png
```

### **Nome do App**
```bash
# Editar buildozer.spec:
title = Seu Nome do App
```

---

## 📱 **Funcionalidades do App Móvel**

### ✅ **Implementadas:**
- **Página inicial** com informações
- **Gerenciador de tarefas** (adicionar, marcar, deletar)
- **Bloco de notas** (adicionar, visualizar, deletar)
- **Acesso ao Q-Acadêmico** (abre no navegador)
- **Interface nativa** com abas
- **Dados salvos localmente**

### 🔄 **Diferenças do App Web:**
- Interface adaptada para mobile
- Navegação por abas
- Botões maiores para touch
- Funciona offline
- Dados salvos no dispositivo

---

## 🚀 **Comandos Rápidos**

```bash
# Testar app
python mobile_app.py

# Construir APK (Linux/WSL)
buildozer android debug

# Limpar build
buildozer android clean

# Ver logs
buildozer android logcat

# Instalar no dispositivo conectado
buildozer android deploy run
```

---

## 📋 **Checklist para APK**

- [ ] Python 3.8+ instalado
- [ ] Kivy instalado
- [ ] Buildozer instalado
- [ ] App testado localmente
- [ ] buildozer.spec configurado
- [ ] Ícone adicionado (opcional)
- [ ] Permissões configuradas
- [ ] APK construído com sucesso
- [ ] APK testado no dispositivo

---

## 🆘 **Ajuda**

### **Problemas Comuns:**
1. **"Permission denied"** → Usar sudo (Linux)
2. **"SDK license"** → Aceitar licenças automaticamente
3. **"Build failed"** → Verificar logs com `buildozer android logcat`

### **Recursos Úteis:**
- [Documentação Kivy](https://kivy.org/doc/stable/)
- [Documentação Buildozer](https://buildozer.readthedocs.io/)
- [Python for Android](https://python-for-android.readthedocs.io/)

---

## 🎉 **Resultado Final**

Após seguir todos os passos, você terá:
- ✅ **APK funcional** para Android
- ✅ **App nativo** (não web view)
- ✅ **Funciona offline**
- ✅ **Dados salvos localmente**
- ✅ **Interface otimizada para mobile**
- ✅ **Acesso ao Q-Acadêmico**

O APK estará em: `bin/appuniversal-1.0-debug.apk` 