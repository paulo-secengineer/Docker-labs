Objetivo:

- Entender as diferenças práticas entre CMD e ENTRYPOINT.
- Testar como o Docker se comporta ao sobrescrever parâmetros no momento da execução.
- Criar combinações com ENTRYPOINT + CMD.

Você está criando um container que executa scripts personalizados. Dependendo da configuração (CMD ou ENTRYPOINT), os usuários poderão (ou não) alterar o comportamento de execução no docker run. Isso é comum em containers CLI, de testes ou utilitários.

1. Criar o diretório
	mkdir lab13-entrypoint-cmd && cd lab13-entrypoint-cmd

2. Criar o script hello.sh
	#!/bin/sh
	echo "Mensagem: $@"

	chmod +x hello.sh

3. Criar Dockerfile com apenas CMD

Dockerfile.cmd

FROM alpine
COPY hello.sh /hello.sh
CMD ["/hello.sh", "Olá via CMD"]

4. Build da imagem
	docker build -t hello-cmd -f Dockerfile.cmd .

5. Testar substituição de argumentos com CMD
	docker run hello-cmd                     										 # Usa o valor padrão "Olá via CMD"
	docker run hello-cmd sh -c 'echo "Outro comando qualquer"'   # Substitui completamente o CMD

6. Criar Dockerfile com apenas ENTRYPOINT

Dockerfile.entrypoint

FROM alpine
COPY hello.sh /hello.sh
ENTRYPOINT ["/hello.sh"]

7. Build e testar
	docker build -t hello-entrypoint -f Dockerfile.entrypoint .
	docker run hello-entrypoint Testando ENTRYPOINT

O ENTRYPOINT fixa o comando a ser executado, e tudo o que for passado no docker run vira argumento.

8. Testar tentativa de sobrescrever o ENTRYPOINT
	docker run hello-entrypoint /bin/sh -c 'echo "tentando ignorar o entrypoint"'

	Saída esperada:
		Mensagem: /bin/sh -c echo tentando ignorar o entrypoint

O ENTRYPOINT é fixo. Mesmo tentando passar outro comando (/bin/sh -c ...), esse comando vira apenas argumento do ENTRYPOINT.
O Docker não ignora o ENTRYPOINT.
Por isso, o script /hello.sh continua sendo executado, e recebe os argumentos /bin/sh -c ...

9. Combinação: ENTRYPOINT + CMD

Dockerfile.combo

FROM alpine
COPY hello.sh /hello.sh
ENTRYPOINT ["/hello.sh"]
CMD ["Mensagem padrão com ENTRYPOINT + CMD"]

10. Build e testes finais
	docker build -t hello-combo -f Dockerfile.combo .
	docker run hello-combo                   					# Usa ENTRYPOINT com CMD como argumento
	docker run hello-combo "Argumento personalizado" 	# ENTRYPOINT permanece, CMD é substituído

CMD pode ser sobrescrito totalmente, inclusive o comando executado.
ENTRYPOINT fixa o comando, mas permite sobrescrever os argumentos.
A combinação ENTRYPOINT + CMD fornece:
	um comando fixo
	argumentos padrão que podem ser substituídos