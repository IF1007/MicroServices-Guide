# MicroServices-Guide
> Um guia simples para os primeiros passos com microsserviços e docker.


Nossa solução é um sistema de fórum de internet, no qual é possível a criação, seleção, edição e exclusão de posts e cadastros de usuários que serão gravados em banco de dados.
Todos os processos estão separados em seus respectivos contêiners e operando com o uso do docker.


## Vamos ao nosso guia

Obs: Primeiramente gostariamos de lembrar que para utilização dos nossos processos é necessário o docker e python instalado e executando em sua máquina.

<b>Arquitetura</b>

![](/images/Arquitetura.PNG)

Como podemos perceber na arquitetura acima, temos um microsserviço relativo ao cadastros, com seu próprio banco de dados, bem como um microsserviço relativo ao fórum em si, com seu próprio banco dados.

Caso você deseje tentar por você mesmo imagine seu projeto como uma grande caixa (que em uso prático séria relativo a uma pasta contendo os dados da aplicação que você deseja contêinerizar, no nosso caso a pasta de servicos e/ou sistemaLogin)nesse primeiro momento de desenvolvimento não se preocupe ainda com as funcionalidades do docker, basta apenas que sua aplicação esteja operante de alguma forma.

<i>Agora que meu sistema está operando, como posso utilizar o docker para acoplá-lo em um contêiner?</i>

É justamente nesse ponto que o <b><i>Dockerfile</i></b> entra para facilitar sua vida, veja o exemplo abaixo que se encontra na nossa pasta <i>servicos</i>

![](/images/dockerfile-servicos.PNG)

<b>Vamos destrinchar esse código:</b>

* FROM python:3-onbuild
    * Esse comando diz ao docker qual versão do python utilizar de seu sistema (para outros tipos de linguagens verificar a documentação do docker)
* COPY . /usr/src/app
    * Esse comando diz ao docker para copiar todo o diretório, representado pelo caractere '.', no qual o dockerfile está inserido para o diretório de destino dentro do docker
* CMD ["python", "app.py"]
    * Esse comando diz ao docker para executar utilizando o python o nosso programa "app.py"
	* Obs: os requisitos necessários para instalação são rodados automaticamente desde que haja um arquivo requirements.txt no diretório onde está o dockerfile

Para testar unitariamente você poderia utilizar os comando do docker build image e então docker run porém nesse tutorial não utilizaremos dessa forma, vamos explicar mais adiante.

Configure corretamente seu docker file passando os comandos necessários para o seu tipo de aplicação.

<b>Destrinchando o dockerfile de login:</b>

![](/images/dockerfile-login.PNG)

* FROM python:3-onbuild
    * Esse comando diz ao docker qual versão do python utilizar de seu sistema (para outros tipos de linguagens verificar a documentação do docker)
* WORKDIR /usr/src/login
    * Esse comando diz ao docker para entrar no diretório dentro do docker (equivalente a um cd /diretorio em linux/windows)
* RUN pip install -r requirements.txt
	* Como já estamos dentro do diretorio no docker execute o comando de pip install para instalar os requisitos passados
* COPY . /usr/src/login
    * Esse comando diz ao docker para copiar todo o diretório, representado pelo caractere '.', no qual o dockerfile está inserido para o diretório de destino dentro do docker
* CMD ["python", "app.py"]
    * Esse comando diz ao docker para executar utilizando o python o nosso programa "app.py"
	* Obs: os requisitos necessários para instalação são rodados automaticamente desde que haja um arquivo requirements.txt no diretório onde está o dockerfile


Certo, dockerfile configurado mas e agora?

Primeiramente é preciso saber em qual porta está rodando sua aplicação. No nosso caso forçamos a nossa aplicação para rodar em localhost na porta 80 (checar os arquivos app.py em ambos os diretórios)

![](/images/app.PNG)

Agora que sabemos onde vai rodar nossa aplicação, vamos a parte mais essencial para deixar nossos sistemas operantes. Vamos ao <b>docker compose</b>.


<b>Destrinchando o docker-compose:</b>

![](/images/docker-compose.PNG)

Primeiramente precisamos definir qual versão, escolhemos a versão 3, e quais serviços utilizar para o nosso docker-compose.

* services:
    * Esse comando diz ao docker quais serão os serviços que o docker utilizará para a execução do programa
*service-login:
	* Esse comando diz ao docker qual será o nome de um dos nossos serviços (a tag/imagem associada ao docker)
	* build: ./sistemaLogin - Diz ao docker para criar a imagem com o nome de sistemaLogin (abstração do comando docker build image com seus parâmetros)
	* volumes: - ./sistemaLogin:/usr/src/login 
		* Como configuramos no dockerfile da pasta sistemaLogin o diretorio usr/src/login passamos o mesmo nessa parte de volume para que a imagem seja criada utilizando esse diretorio.
	* ports: - 5002:80
		* Porta no qual será executada nossa aplicação, mapeia o que está na porta da direita (aplicação) para a porta da esquerda (de fato onde será executado o sistema)
*service-blog:
	* Esse comando diz ao docker qual será o nome de um dos nossos serviços (a tag/imagem associada ao docker)
	* build: ./servicos - Diz ao docker para criar a imagem com o nome de sistemaLogin (abstração do comando docker build image com seus parâmetros)
	* volumes: - ./servicos:/usr/src/app 
		* Como configuramos no dockerfile da pasta servicos o diretorio usr/src/app passamos o mesmo nessa parte de volume para que a imagem seja criada utilizando esse diretorio.
	* ports: - 5001:80
		* Porta no qual será executada nossa aplicação, mapeia o que está na porta da direita (aplicação) para a porta da esquerda (de fato onde será executado o sistema)
	*depends_on: - service-login
		* Esse comando diz ao docker que esse servico que estamos tentando rodar depende dos resultados da aplicação service-login para alguns de seus funcionamentos, gerando assim uma relação entre as aplicações
		
Perceba que com algumas linhas de configuração vamos atingir nosso resultado esperado, que ambas as aplicações estejam rodando corretamente e sejam capazes de se comunicar entre si.

E, para finalizar...

## Execução do programa

Com o docker instalado e rodando, abra nosso repositório em um terminal e utilize o comando:

```sh
docker-compose up
```

o docker automaticamente instalará todas as dependências e, após a instalação e execução, vá ao seu browser de preferência e utilize o seguinte host:

```sh
localhost:5001
```

E <i>Voilá</i> nosso sistema estará rodando em sua máquina, sinta-se a vontade para explorar da maneira que bem entender.


<b>Hope you enjoy!</b>