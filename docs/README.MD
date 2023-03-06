# Orbit Export Comments Backend

<br>

## Descrição do Projeto:


---



O Orbit Export Comments é um web app que se recebe uma lista no formato .xlsx do usuário e utiliza a API Export Comments para extrair os comentários de cada link de rede social informado.

O Backend do projeto foi desenvolvido usando a linguagem Python e o framwork Flask

<br>

## Pré-requisitos:


---



*   Python 3.10.10
*   VS Code 1.76.0 (ou outro editor de código)

<br>

##Como editar o projeto localmente:


---



1.   Abra o terminal do VSCode e clone o repositório do projeto do github com o seguinte comando:
  ```
  git clone https://github.com/FlavioTomeOrbitDS/export-comments-backend
  ```



2.  Crie e ative um Virtual Enviroment:


*   Um virtual enviroment é utlizado para encapsular o projeto dentro de um ambiente próprio, onde só serão instaladas as bibliotecas necessárias para o funcionanemto da aplicação. Este módulo já vem instado junto com o Python;



*   Dentro do diretório principal do projeto crie um novo ambiente virtual chamado venv com o seguinte comando:   
```
PS ...\export-comments-backend>python -m venv venv
```

* Ative o virtual enviroment:
```
  PS ...\export-comments-backend>venv\Scripts\activate
```
* Caso o virtual enviroment tenha sido ativado corretamente, o path do projeto no terminal ficará com (venv) logo no início
```
(venv) PS ...\export-comments-backend>
```
<br>

3. Com o virtual enviroment ativado, você pode instalar as bibliotecas do projeto:

* A Lista das bibliotecas do projeto está em um arquivo chamado **requirements.txt**. Instale as bibliotecas com o seguinte comando:
```
(venv) PS ...\export-comments-backend>pip install -r requirements.txt
```

4. Finalment, assim que todas as bibliotecas forem instaladas, você poderá rodar o backend do Orbit Export Comments:
```
(venv) PS ...\export-comments-backend>flask run
```

5. A API estará disponível em :[ http://localhost:5000](https://)

<br>

## API Endpoints
---
 ### POST: /api/generateEndpointsFromList
* Payload:<br>
Este endpoint recebe uma lista de links de redes sociais e retorna os endpoints para o download dos arquivos gerados pelo Export Comments.
```
{
  "list_of_endpoints": [
    "https://www.facebook.com/my-page/posts/123",
    "https://www.instagram.com/p/abc"
  ]
}
```
* Resposta:
```
{
  "download_url_list": [
    "instagram-comments64...252-CofWZpKjMIc.xlsx",
    "instagram-comments64...a3d-CoqH9lkDHr7.xlsx"
  ]
}
```

### POST: /api/downloadfiles
* Payload:<br>
Este Endpoint recebe uma url de download que foi gerada pela generateEndpointsFromList. Como resposta, retorna um um arquivo no formato .xlsx que é enviado como binário para que possa ser baixado pelo browser do usuário
```
{
  "endpoint": 
    "instagram-comments64...252-CofWZpKjMIc.xlsx"
}
```
* Reposta:
```
return send_file(
        buffer,
        download_name="data.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
```

<br>

## Deploy no Google Cloud Plataform
---
O Orbit Export Comments Backend é executado no Google Cloud Run por meio de um container Docker. Para fazer o deploy no GCP, você deve sergir os seguintes passos:
1.   Criar um projeto no GCP e ativar as API's necessárias. 
2.   Ativar a Cloud Run API
3.   Criar uma imagem de container Docker do projeto
4.   Faça o git clone do projeto no Google Cloud
5.   Fazer o upload da imagem do containder no Google Container Registry.
6.   Fazer o Deploy do container e executá-lo por meio do Google Cloud Run


1. ### Criando um novo projeto do Google Cloud Plataform
Para criar um novo projeto no Google Cloud Platform, siga estes passos:
* Acesse o Console do Google Cloud Platform (https://console.cloud.google.com/).
* Clique no botão "Selecionar Projeto" localizado no canto superior direito da página.
* Clique no botão "Novo Projeto".
* Insira um nome para o projeto.
* (Opcional) Selecione uma organização ou pasta para o projeto.
* Clique no botão "Criar".
* Aguarde alguns instantes enquanto o projeto é criado.
* Uma vez que o projeto esteja pronto, você será redirecionado para a página do Console do Google Cloud Platform com o novo projeto selecionado.  
Para ativar a API do Google Cloud Run 

<br>

2. ### Ativando a Google Cloud API:  
* No menu de navegação, selecione "APIs e Serviços" e clique em "Biblioteca de APIs".  
* Na barra de busca, digite "Cloud Run" e selecione a opção "Cloud Run API".  
* Clique no botão "Ativar".

<br>

3. ### Criando o container Docker do Projeto:  
No diretório raiz do projeto, crie um novo arquivo chamado "Dockerfile".  
Abra o Dockerfile no editor e insira o código a seguir:
```
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python"]
CMD [ "app.py" ]
```
Salve e feche o arquivo.

<br>

4. ### Clonando o projeto no Google Cloud:
* Abra o terminal do GCP e execute o comando git clone [URL do repositório] para clonar o repositório do projeto no github para o Google Cloud. Substitua [URL do repositório] pela URL do repositório que deseja clonar.
* Insira as credenciais de login do Git, se solicitado.
* Use o comando **CD** para navegar até o diretório raiz do projeto no Google Cloud.

<br>

5. ### Fazendo o upload do containder no Google Container Registry.
O Container Registry é um serviço de armazenamento e gerenciamento de containers da Google Cloud Plataform.
Para fazer o upload de um container siga os seguintes passos:
* Certifique-se de que o Docker esteja instalado em sua máquina local.
* Faça o build da imagem do Docker para o Google Container Registry usando o comando:
```
 docker build -t [TAG_NAME] gcr.io/[PROJECT_ID]/[IMAGE_NAME].
```
Abra o Console do Google Cloud Platform (https://console.cloud.google.com/run).

Clique no botão "Criar Serviço" e selecione o projeto em que deseja implantar o serviço.

Escolha um nome para o serviço e selecione a imagem do Docker que você acabou de fazer o push.

Escolha as configurações de implantação necessárias, como a região, as opções de escalonamento e as variáveis ​​de ambiente.

Clique no botão "Implantar" para implantar o contêiner Docker no Google Cloud Run.








