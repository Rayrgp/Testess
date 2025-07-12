// Variáveis globais
let currentSection = 'home';

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadTasks();
    loadNotes();
});

// Inicializar aplicativo
function initializeApp() {
    setupNavigation();
    setupMobileMenu();
    setupEventListeners();
}

// Configurar navegação
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('data-section');
            showSection(section);
            
            // Atualizar links ativos
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Fechar menu mobile se estiver aberto
            const sidebar = document.getElementById('sidebar');
            if (sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        });
    });
}

// Configurar menu mobile
function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const closeMenu = document.getElementById('closeMenu');
    const sidebar = document.getElementById('sidebar');
    
    menuToggle.addEventListener('click', function() {
        sidebar.classList.add('open');
    });
    
    closeMenu.addEventListener('click', function() {
        sidebar.classList.remove('open');
    });
    
    // Fechar menu ao clicar fora
    document.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    });
}

// Configurar event listeners
function setupEventListeners() {
    // Tarefas
    const addTaskBtn = document.getElementById('addTaskBtn');
    const saveTaskBtn = document.getElementById('saveTaskBtn');
    const taskInput = document.getElementById('taskInput');
    
    addTaskBtn.addEventListener('click', function() {
        const container = document.getElementById('taskInputContainer');
        container.style.display = 'flex';
        taskInput.focus();
    });
    
    saveTaskBtn.addEventListener('click', saveTask);
    taskInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            saveTask();
        }
    });
    
    // Notas
    const addNoteBtn = document.getElementById('addNoteBtn');
    const saveNoteBtn = document.getElementById('saveNoteBtn');
    
    addNoteBtn.addEventListener('click', function() {
        const container = document.getElementById('noteInputContainer');
        container.style.display = 'block';
        document.getElementById('noteTitleInput').focus();
    });
    
    saveNoteBtn.addEventListener('click', saveNote);
}

// Mostrar seção
function showSection(sectionName) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionName;
    }
}

// ===== FUNÇÕES DE TAREFAS =====

// Carregar tarefas
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
    }
}

// Exibir tarefas
function displayTasks(tasks) {
    const tasksList = document.getElementById('tasksList');
    tasksList.innerHTML = '';
    
    if (tasks.length === 0) {
        tasksList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">Nenhuma tarefa encontrada. Adicione sua primeira tarefa!</p>';
        return;
    }
    
    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        tasksList.appendChild(taskElement);
    });
}

// Criar elemento de tarefa
function createTaskElement(task) {
    const taskDiv = document.createElement('div');
    taskDiv.className = `task-item ${task.completed ? 'completed' : ''}`;
    taskDiv.innerHTML = `
        <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} onchange="toggleTask(${task.id})">
        <span class="task-title">${task.title}</span>
        <button class="delete-task" onclick="deleteTask(${task.id})">
            <i class="fas fa-trash"></i>
        </button>
    `;
    return taskDiv;
}

// Salvar tarefa
async function saveTask() {
    const taskInput = document.getElementById('taskInput');
    const title = taskInput.value.trim();
    
    if (!title) {
        alert('Por favor, digite uma tarefa!');
        return;
    }
    
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title })
        });
        
        if (response.ok) {
            taskInput.value = '';
            document.getElementById('taskInputContainer').style.display = 'none';
            loadTasks();
        }
    } catch (error) {
        console.error('Erro ao salvar tarefa:', error);
        alert('Erro ao salvar tarefa!');
    }
}

// Alternar tarefa
async function toggleTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}/toggle`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Erro ao alternar tarefa:', error);
    }
}

// Deletar tarefa
async function deleteTask(taskId) {
    if (!confirm('Tem certeza que deseja deletar esta tarefa?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/tasks', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: taskId })
        });
        
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Erro ao deletar tarefa:', error);
        alert('Erro ao deletar tarefa!');
    }
}

// ===== FUNÇÕES DE NOTAS =====

// Carregar notas
async function loadNotes() {
    try {
        const response = await fetch('/api/notes');
        const notes = await response.json();
        displayNotes(notes);
    } catch (error) {
        console.error('Erro ao carregar notas:', error);
    }
}

// Exibir notas
function displayNotes(notes) {
    const notesList = document.getElementById('notesList');
    notesList.innerHTML = '';
    
    if (notes.length === 0) {
        notesList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">Nenhuma nota encontrada. Crie sua primeira nota!</p>';
        return;
    }
    
    notes.forEach(note => {
        const noteElement = createNoteElement(note);
        notesList.appendChild(noteElement);
    });
}

// Criar elemento de nota
function createNoteElement(note) {
    const noteDiv = document.createElement('div');
    noteDiv.className = 'note-item';
    
    const date = new Date(note.created_at).toLocaleDateString('pt-BR');
    
    noteDiv.innerHTML = `
        <div class="note-header">
            <h3 class="note-title">${note.title}</h3>
            <button class="delete-task" onclick="deleteNote(${note.id})">
                <i class="fas fa-trash"></i>
            </button>
        </div>
        <div class="note-content">${note.content}</div>
        <div class="note-date">Criada em: ${date}</div>
    `;
    return noteDiv;
}

// Salvar nota
async function saveNote() {
    const titleInput = document.getElementById('noteTitleInput');
    const contentInput = document.getElementById('noteContentInput');
    
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();
    
    if (!title || !content) {
        alert('Por favor, preencha o título e o conteúdo da nota!');
        return;
    }
    
    try {
        const response = await fetch('/api/notes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content })
        });
        
        if (response.ok) {
            titleInput.value = '';
            contentInput.value = '';
            document.getElementById('noteInputContainer').style.display = 'none';
            loadNotes();
        }
    } catch (error) {
        console.error('Erro ao salvar nota:', error);
        alert('Erro ao salvar nota!');
    }
}

// Deletar nota
async function deleteNote(noteId) {
    if (!confirm('Tem certeza que deseja deletar esta nota?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/notes', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: noteId })
        });
        
        if (response.ok) {
            loadNotes();
        }
    } catch (error) {
        console.error('Erro ao deletar nota:', error);
        alert('Erro ao deletar nota!');
    }
}



// ===== FUNÇÕES DE APLICAÇÕES EXTERNAS =====

// Abrir Q-Acadêmico na mesma aba
function openQAcademico() {
    const url = 'https://academico.iff.edu.br/qacademico/index.asp?t=1001';
    window.location.href = url;
}

// Abrir Q-Acadêmico em nova aba
function openQAcademicoNewTab() {
    const url = 'https://academico.iff.edu.br/qacademico/index.asp?t=1001';
    window.open(url, '_blank');
}

// Mostrar formulário de login do Q-Acadêmico
function showQAcademicoLogin() {
    const loginForm = document.getElementById('qacademicoLoginForm');
    const actions = document.querySelector('.app-actions');
    
    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        actions.style.display = 'none';
        document.getElementById('qacademicoUsername').focus();
    } else {
        loginForm.style.display = 'none';
        actions.style.display = 'flex';
    }
}

// Fazer login no Q-Acadêmico
async function loginQAcademico() {
    const username = document.getElementById('qacademicoUsername').value.trim();
    const password = document.getElementById('qacademicoPassword').value.trim();
    
    if (!username || !password) {
        showNotification('Por favor, preencha todos os campos!', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/qacademico-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Redirecionando para o Q-Acadêmico...', 'success');
            
            // Criar um formulário temporário para enviar os dados de login
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = 'https://academico.iff.edu.br/qacademico/index.asp?t=1001';
            form.target = '_blank';
            
            const usernameField = document.createElement('input');
            usernameField.type = 'hidden';
            usernameField.name = 'txtUsuario';
            usernameField.value = username;
            
            const passwordField = document.createElement('input');
            passwordField.type = 'hidden';
            passwordField.name = 'txtSenha';
            passwordField.value = password;
            
            form.appendChild(usernameField);
            form.appendChild(passwordField);
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
            
            // Limpar formulário
            document.getElementById('qacademicoUsername').value = '';
            document.getElementById('qacademicoPassword').value = '';
            showQAcademicoLogin(); // Esconder formulário
        } else {
            showNotification(result.error || 'Erro ao fazer login', 'error');
        }
    } catch (error) {
        console.error('Erro ao fazer login:', error);
        showNotification('Erro ao conectar com o servidor', 'error');
    }
}

// ===== FUNÇÕES UTILITÁRIAS =====

// Mostrar notificação
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Estilos da notificação
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#667eea'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Adicionar estilos de animação para notificações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style); 