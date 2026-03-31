Objetivo:

Criar uma aplicação simples em HTML.

- Escrever um Dockerfile básico para empacotar a aplicação com Nginx.
- Construir a imagem com docker build.
- Executar a imagem criada como container.
- Validar o funcionamento da aplicação.
- Verificar camadas da imagem e uso de espaço.

1. Preparar a estrutura do projeto

Crie uma pasta chamada meu-site:
	mkdir meu-site && cd meu-site

Dentro dela, crie um arquivo index.html com conteúdo simples:
	<!DOCTYPE html>
	<html lang="pt-BR">
	<head>
  	<meta charset="UTF-8" />
  	<title>Meu Site no Docker</title>
	</head>
	<body>
  	<h1>Olá, mundo Dockerizado!</h1>
  	<p>Esta página está sendo servida por um container Nginx customizado.</p>
	</body>
	</html>

2. Criar o Dockerfile

Na mesma pasta, crie um arquivo chamado Dockerfile (sem extensão) com o seguinte conteúdo:

# Usando imagem base oficial do Nginx
FROM nginx:latest

# Removendo o conteúdo padrão do Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiando o site estático para o diretório padrão do Nginx
COPY index.html /usr/share/nginx/html/

# Expondo a porta padrão do Nginx
EXPOSE 80

3. Construir a imagem

Execute o comando abaixo na raiz do projeto para construir a imagem:
	docker build -t meu-nginx-site .

O -t define o nome da imagem. O . indica que o Docker deve usar o Dockerfile da pasta atual.

4. Verificar a imagem criada
	docker images

Você verá a imagem meu-nginx-site listada entre as disponíveis.

5. Rodar o container com a imagem criada
	docker run -d --name container-site -p 8085:80 meu-nginx-site

Acesse via navegador: http://localhost:8085

Ou via terminal:
	curl http://localhost:8085

Verificar detalhes com inspect e jq (opcional)

Ver camadas da imagem:
	docker inspect meu-nginx-site | jq '.[0].RootFS.Layers'

6. Parar e remover
	docker stop container-site
	docker rm container-site
	docker rmi meu-nginx-site
