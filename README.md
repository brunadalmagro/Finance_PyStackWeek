# Finance_PyStackWeek

### Status

# Descrição:
Esta é aplicação web desenvolvida com Django, que permite aos usuários gerenciar e definir metas de planejamento financeiro para diferentes categorias. 
- Os usuários podem acompanhar e atualizar os valores planejados para cada categoria, ajudando-os a organizar suas finanças e estabelecer metas realistas para gastos e economias.

# Recursos e funcionalidades na `Home`:

>Seção de Entradas e Saídas:
>Exibe o total de entradas e o total de saídas, com cards clicáveis que redireciona para a página de visualização de entradas e saídas na conta.
-----------------------------------------------------------------------------------------------------------------------------------
>Seção de Saldo e Contas:
>Exibe o saldo total e lista as contas disponíveis, cada conta é mostrada com seu apelido e valor atual.
>> Inclui um botão "Gerenciar contas" para redirecionar para uma página de gerenciamento de contas.

-----------------------------------------------------------------------------------------------------------------------------------
>Seção de Saldo Mensal:
>Exibe o saldo mensal atual.
>>Inclui um botão para gerenciar os dados mensais.

-----------------------------------------------------------------------------------------------------------------------------------
>Seção de Planejamento:
>Exibe opções para definir o planejamento financeiro e visualizar o planejamento existente.
>>Inclui botões "Definir planejamento" e "Ver planejamento" que redirecionam para acesso aos planejamentos.

-----------------------------------------------------------------------------------------------------------------------------------
>Seção de Equilíbrio Financeiro:
>Exibe barras de progresso para mostrar o percentual de gastos essenciais e não essenciais.
>>Inclui um botão para alterar as categorias de gastos essenciais.

-----------------------------------------------------------------------------------------------------------------------------------
>Seção de Gerenciamento de Contas:
>Exibe estatísticas relacionadas às contas, como contas próximas do vencimento e contas vencidas.
>>Inclui um botão "Ver mais" para redirecionar para uma página com mais detalhes sobre as contas.

---------------------------------------------------------------------------------------------

_**Outras funcionalidades técnicas**_
- É possível realizar um cadastro ao iniciar o app, com login e senha;
- Ao acessar a página "Definir Planejamento" onde são exibidas diferentes categorias relacionadas ao planejamento financeiro, como despesas, investimentos, metas de economia, etc. Podendo digitar os valores planejados para cada categoria e salvá-los;
- Logo após você pode viasualizar esses valores salvos na área 'Ver Planejamento', assim sussede com as demais funcionalidaes;
- O app tem uma resposta dinâmica das alterações em banco de dados realizadas, renderizando-as nas sessões correspondentes;
- Validação do método de entrada, referente a cada sessão;
- Atualização do valor da categoria: Quando um usuário atualiza um valor planejado para uma categoria, o valor é armazenado e atualizado no banco de dados;
- Mensagens de sucesso e erro: O aplicativo exibe mensagens de sucesso ou erro para informar o usuário sobre o resultado da ação realizada;

============================================================================
## Contribuição
--> Se você quiser contribuir para o desenvolvimento, sinta-se à vontade para abrir um pull request. Será um prazer receber contribuições para tornar o aplicativo ainda melhor.
