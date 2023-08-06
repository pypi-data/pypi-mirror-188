# Trabalho GCES
Aluno: Antonio Igor Carvalho
Matrícula: 180030264

## Containerização do Banco
O banco foi containerizado utilizando a imagem oficial do postgres
![BancoDocker](./prints/banco_docker.png)

## Containerização da biblioteca + Banco
A biblioteca foi containerizada com uma imagem criada por mim, e o container do app, banco e metabase utilizando o docker-compose
![BancoAppDocker](./prints/banco_app_docker.png)

## Publicação da biblioteca
A publicação da biblioteca foi feita no pypi, utilizando o poetry
![Pypi](./prints/pypi.png)
https://pypi.org/project/trabalho-de-gces/

## Documentação automatizada
A documentação é atualizada juntamente com a build da imagem
![Documentação](./prints/documentacao.png)

## Integração contínua
A build, atualização da documentação e teste são feitos quando ocorre a publicação de um novo commit
![CI](./prints/ci.png)
## Deploy contínuo
A publicação da biblioteca é feita automaticamente quando a varivável de ambiente 'current_version' é atualizada
![Pypi](./prints/pypi.png)
