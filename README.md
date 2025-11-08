# genaralmathcalculetor
Um site com calculadores para uso em algumas provas de escolas dos criadores desse site e para outras pessoas aprenderem matemática mais facilmente.

## Dificuldade: Manter o Tema Escuro Após Atualizar a Página
Durante o desenvolvimento, uma das principais dificuldades foi fazer com que o tema escuro permanecesse ativo mesmo depois de atualizar a página ou fechar o navegador.  
Por padrão, ao recarregar o site, o navegador apagava o estado do tema e voltava para o modo claro.

### Solução
Para resolver isso, foi usado o `localStorage`, que guarda o tema selecionado diretamente no navegador do usuário.  
Assim, quando a página é carregada novamente, o JavaScript verifica o valor salvo no `localStorage` e aplica automaticamente o tema correspondente (claro ou escuro), garantindo que a preferência do usuário seja mantida.
