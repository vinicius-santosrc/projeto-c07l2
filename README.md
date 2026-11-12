# Projeto Banco de Dados I - Plataforma de Jogos Digitais

## Integrantes
- Vinícius da Silva Santos - 637 - GES
- Marcelo Henrique da Silva Costa - 628 - GES

## Tema
Plataforma de jogos digitais inspirada na Steam.

A ideia é permitir o cadastro de usuários, perfis, jogos, desenvolvedoras, categorias e compras realizadas pelos usuários

Cada usuário possui um perfil. Uma desenvolvedora pode possuir vários jogos e cada jogo pertence a uma categoria. Além disso, um usuário pode comprar vários jogos e um mesmo jogo pode ser comprado por vários usuários.

## Entidades
- Usuario
- Perfil
- Desenvolvedora
- Categoria
- Jogo
- Compra

## Relacionamentos
- Usuario 1:1 Perfil
- Desenvolvedora 1:N Jogo
- Categoria 1:N Jogo
- Usuario N:M Jogo, utilizando Compra como tabela intermediária


---

# 2ª Entrega do Projeto — STEAM_DB

Banco de dados inspirado em uma loja de jogos digitais (estilo Steam), implementado em SQL a partir do modelo da 1ª entrega.

- **Arquivo do Script:** `steam_db_script.sql`

> O script recria o banco do zero (`DROP DATABASE IF EXISTS STEAM_DB`), Para ser executado varias vezes.

## 1. Criação do banco e das tabelas (DDL)

Seção 1 do script. Usa `DROP DATABASE IF EXISTS`, `CREATE DATABASE`, `USE` e `CREATE TABLE`, com os mesmos tipos, chaves e restrições do modelo `steam_db.mwb`:

- `PRIMARY KEY` com `AUTO_INCREMENT` nos ids (na `compra`, a PK é composta por `id_usuario` e `id_jogo`);
- `NOT NULL` nos campos obrigatórios e `UNIQUE` no e-mail do usuário e no `id_usuario` do perfil (garante o 1:1);
- `DECIMAL(10,2)` para valores em reais e `DATETIME` para a data da compra;
- `FOREIGN KEY` com regras de integridade:
  - `ON DELETE CASCADE` em `perfil → usuario` e `compra → usuario`: ao apagar um usuário, seu perfil e suas compras são apagados junto;
  - `ON DELETE RESTRICT` em `jogo → desenvolvedora`, `jogo → categoria` e `compra → jogo`: não é possível apagar uma desenvolvedora, categoria ou jogo que ainda está em uso.

## 2. Inserção de dados

Seção 2 do script. Todas as tabelas têm **no mínimo 5 registros**:

| Tabela | Registros |
|---|---|
| `usuario` | 6 |
| `perfil` | 6 |
| `desenvolvedora` | 7 |
| `categoria` | 6 |
| `jogo` | 11 |
| `compra` | 13 |

- Os dados são inseridos respeitando as dependências: primeiro as tabelas independentes (`usuario`, `desenvolvedora`, `categoria`), depois as dependentes (`perfil`, `jogo`) e por fim `compra`.
- As senhas são gravadas com `SHA2(..., 256)` (hash), e não em texto puro.
- O usuário **Felipe (id 6)** ainda não tem compras: ele é usado no teste da procedure.

## 3. Comandos DML e TCL e por que foram usados

| Comando | O que faz | Por que foi usado |
|---|---|---|
| `INSERT` | Popula todas as tabelas | Criar os dados necessários para testar consultas, view, function e procedure. |
| `UPDATE jogo SET preco = fn_preco_com_desconto(preco, 20) WHERE id_jogo = 2` | Aplica 20% de desconto no Cyberpunk 2077 | Simula uma promoção e mostra a function sendo usada dentro de um `UPDATE`. |
| `UPDATE perfil SET biografia = ... WHERE id_usuario = 1` | Altera a biografia da Ana | Simula a edição do perfil pelo próprio usuário. |
| `CALL sp_registrar_compra(6, 4, 'PIX')` | Felipe compra *Stardew Valley* | Demonstra a procedure registrando uma compra pelo preço atual do jogo. |
| `DELETE FROM compra WHERE id_usuario = 6 AND id_jogo = 4` | Remove a compra | Simula o **reembolso**. O `WHERE` usa a PK composta para apagar somente aquela compra. |
| `START TRANSACTION`, `SAVEPOINT`, `ROLLBACK TO`, `COMMIT` | Aplica um desconto exagerado, desfaz só ele e aplica o correto | Demonstra o controle de transações (TCL): o `ROLLBACK TO` desfaz apenas o que veio depois do `SAVEPOINT`. |
| `START TRANSACTION` + `INSERT` + `ROLLBACK` | Insere uma compra de valor negativo e desfaz tudo | Testa o trigger sem deixar lixo no banco. |

`SET SQL_SAFE_UPDATES = 0` desativa o modo seguro do Workbench, que bloqueia `UPDATE`/`DELETE` sem chave no `WHERE`.

## 4. Usuários e ROLE (DCL)

Seção 7 do script.

| Objeto | Descrição |
|---|---|
| `role_steam_consulta` | **ROLE compartilhada pelos dois usuários.** Permissão `SELECT` em todas as tabelas do banco `STEAM_DB`. |
| `role_steam_operador` | *(extra)* `INSERT` e `UPDATE` na tabela `compra`; depois o `UPDATE` é retirado com `REVOKE`. |
| `usr_analista` | Usuário somente leitura (relatórios). Recebe apenas `role_steam_consulta`. |
| `usr_atendente` | Usuário de atendimento. Recebe `role_steam_consulta` **e** `role_steam_operador`. |

Comandos usados: `CREATE ROLE`, `CREATE USER`, `GRANT` (na role e da role para o usuário), `SET DEFAULT ROLE`, `REVOKE`, `FLUSH PRIVILEGES` e `SHOW GRANTS`.

**Por que usar ROLE?** Em vez de repetir o `GRANT` para cada usuário, as permissões são definidas uma vez na role e depois atribuídas aos usuários. Se a permissão mudar, basta alterar a role. Os dois usuários se relacionam justamente por compartilharem `role_steam_consulta`.

Resultado final: o analista só lê; o atendente lê e também insere compras (mas não altera, por causa do `REVOKE UPDATE`).

Senhas de exemplo (apenas para fins acadêmicos): `Analista@123` e `Atendente@123`.

## 5. Consultas com JOIN

Seção 5 do script. Os três tipos de relacionamento são cobertos:

| # | Relacionamento | Consulta | Técnicas |
|---|---|---|---|
| 5.1 | **1:1** | Usuários com seus perfis | `INNER JOIN`, `ORDER BY` |
| 5.2 | **1:N** | Jogos com a sua desenvolvedora | `INNER JOIN`, `ORDER BY` |
| 5.3 | **1:N** | Quantidade de jogos e preço médio por desenvolvedora | `INNER JOIN`, `COUNT`, `AVG`, `ROUND`, `GROUP BY` |
| 5.4 | **1:N** | Jogos de Aventura entre R$ 15 e R$ 50 | `INNER JOIN`, `WHERE`, `AND`, `BETWEEN` |
| 5.5 | **N:M** | Jogos de cada usuário | `INNER JOIN` em 4 tabelas |
| 5.6 | **N:M** | Usuários que têm mais de 2 jogos | `COUNT`, `SUM`, `GROUP BY`, `HAVING` |
| 5.7 | **N:M** | Os 3 jogos mais vendidos | `COUNT`, `SUM`, `GROUP BY`, `ORDER BY`, `LIMIT` |
| 5.8 | **N:M** | Compras por PIX feitas em 2023 | `INNER JOIN`, `WHERE`, `BETWEEN` |

## 6. Function, Procedure, Trigger e View

### Function — `fn_preco_com_desconto(p_preco, p_percentual)`
Recebe um preço e um percentual e retorna o preço com desconto (`DECIMAL(10,2)`).
**Por quê:** a conta de desconto é usada em mais de um lugar (promoção no `UPDATE`, preço promocional no `SELECT`). Em uma function ela fica escrita uma única vez e pode ser usada dentro de qualquer consulta, como as funções nativas do MySQL. É `DETERMINISTIC` (mesma entrada, mesma saída) e não altera dados.


### Procedure — `sp_registrar_compra(p_id_usuario, p_id_jogo, p_forma_pagamento)`
Registra a compra de um jogo.
**Por quê:** comprar envolve várias regras (o usuário existe? o jogo existe? o usuário já tem o jogo? qual é o preço?). Centralizar isso na procedure garante que toda compra siga as mesmas regras e que o valor pago venha do preço do jogo, e não de um valor digitado errado. Usa parâmetros `IN`, variáveis (`DECLARE`), `IF / ELSEIF / ELSE` e devolve uma mensagem em `Resultado`.


### Trigger — `trg_compra_valor_check` (`BEFORE INSERT` em `compra`)
Se o `valor_pago` for negativo, troca o valor por `0` antes de gravar (`SET NEW.valor_pago = 0`).
**Por quê:** garante a regra **no próprio banco**, qualquer que seja a aplicação ou o usuário que faça o `INSERT`. Foi usado `BEFORE` porque só nesse momento é possível alterar o `NEW` antes de o dado ser gravado.

### View — `vw_biblioteca_usuario`
Une `usuario`, `perfil`, `compra`, `jogo`, `categoria` e `desenvolvedora`.
**Por quê:** essa consulta com 6 tabelas é muito usada. A view a guarda com um nome, simplifica o uso (`SELECT * FROM vw_biblioteca_usuario`) e ainda **esconde colunas sensíveis** (como `email` e `senha`), permitindo dar acesso à view sem expor a tabela `usuario` inteira.


## 7. Implementações extras

1. **Segunda ROLE (`role_steam_operador`)** — separa o perfil de "consulta" do perfil "operacional", e usa `REVOKE` para tirar a permissão de `UPDATE` do atendente (princípio do menor privilégio).
2. **Controle de transações (TCL)** — uso de `START TRANSACTION`, `SAVEPOINT`, `ROLLBACK TO` e `COMMIT` em dois exemplos práticos (seção 3).
3. **Senhas com hash** (`SHA2`) nos dados de exemplo.
4. **Consultas adicionais** com `BETWEEN`, `LIMIT` e filtros combinados.
