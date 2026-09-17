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
