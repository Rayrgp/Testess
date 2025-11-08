// ===== Alternar abas =====
const botoesAbas = document.querySelectorAll('.botao-aba'); // todos os botões de aba
const conteudosAbas = document.querySelectorAll('.conteudo-aba'); // todas as abas de conteúdo

botoesAbas.forEach(botao => {
  botao.addEventListener('click', () => {

    // Remove ativo de todas as abas(percorre todas as abas)
    botoesAbas.forEach(b => b.classList.remove('ativo'));
    // Esconde todos os conteúdos(percorre todos os conteúdos)
    conteudosAbas.forEach(c => c.classList.add('d-none'));

    // Ativa a aba clicada
    botao.classList.add('ativo');
    const alvo = document.querySelector(botao.dataset.alvo);
    alvo.classList.remove('d-none');
  });
});

// ===== Alternar inputs da matriz determinante =====
const tamanhoMatriz = document.getElementById('tamanho-matriz');
const inputs2x2 = document.getElementById('inputs-2x2');
const inputs3x3 = document.getElementById('inputs-3x3');

tamanhoMatriz.addEventListener('change', () => {
  if(tamanhoMatriz.value === '2') {
    inputs2x2.classList.remove('d-none');
    inputs3x3.classList.add('d-none');
  } else {
    inputs2x2.classList.add('d-none');
    inputs3x3.classList.remove('d-none');
  }
});



// Seleciona o select do tamanho do sistema
const tamanhoSistema = document.getElementById('tamanho-sistema');
// Seleciona os containers das matrizes
const inputs2x2Sistema = document.getElementById('inputs-2x2-sistema');
const inputs3x3Sistema = document.getElementById('inputs-3x3-sistema');

// Adiciona evento de mudança no select
tamanhoSistema.addEventListener('change', () => {
  if (tamanhoSistema.value === '2') {
    inputs2x2Sistema.classList.remove('d-none'); // mostra 2x2
    inputs3x3Sistema.classList.add('d-none');    // esconde 3x3
  } else {
    inputs2x2Sistema.classList.add('d-none');    // esconde 2x2
    inputs3x3Sistema.classList.remove('d-none'); // mostra 3x3
  }
});
const botaoTema = document.getElementById('botao-tema');
const root = document.documentElement;

// Função para aplicar o tema
function aplicarTema(tema) {
  if (tema === 'claro') {
    root.style.setProperty('--cor-fundo', '#FDF5F5');
    root.style.setProperty('--cor-texto', '#2B0A0A');
    root.style.setProperty('--cor-texto-secundaria', '#FFFFFF');
    root.style.setProperty('--cor-fundo-input', '#FFFFFF');
    root.style.setProperty('--cor-caixa-fundo', 'rgba(255, 245, 245, 0.9)');
    root.style.setProperty('--cor-container-sistema', 'rgba(255, 245, 245, 0.85)');
    root.style.setProperty('--cor-display', 'rgba(255, 180, 180, 0.2)');
    botaoTema.textContent = 'Tema Escuro';
  } else {
    root.style.setProperty('--cor-fundo', '#0A0A0A');
    root.style.setProperty('--cor-texto', '#E6DEFF');
    root.style.setProperty('--cor-texto-secundaria', '#FFFFFF');
    root.style.setProperty('--cor-fundo-input', '#121212');
    root.style.setProperty('--cor-caixa-fundo', 'rgba(18, 18, 18, 0.85)');
    root.style.setProperty('--cor-container-sistema', 'rgba(18, 18, 18, 0.75)');
    root.style.setProperty('--cor-display', 'rgba(180, 100, 100, 0.1)');
    botaoTema.textContent = 'Tema Claro';
  }
  // Salva o tema atual
  localStorage.setItem('tema', tema);
}

// Quando carregar a página, aplica o tema salvo (ou escuro como padrão)
const temaSalvo = localStorage.getItem('tema') || 'escuro';
aplicarTema(temaSalvo);

// Ao clicar, alterna o tema
botaoTema.addEventListener('click', () => {
  const temaAtual = localStorage.getItem('tema') === 'claro' ? 'escuro' : 'claro';
  aplicarTema(temaAtual);
});
