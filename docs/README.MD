# Orbit Export Comments Backend

\

## Descrição do Projeto:


---



O Orbit Export Comments é um web app que se recebe uma lista no formato .xlsx do usuário e utiliza a API Export Comments para extrair os comentários de cada link de rede social informado.

O Backend do projeto foi desenvolvido usando a linguagem Python e o framwork Flask

\
## Pré-requisitos:


---



*   Python 3.10.10
*   VS Code 1.76.0 (ou outro editor de código)

\

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
\
3. Com o virtual enviroment ativado, você pode instalar as bibliotecas do projeto:

* A Lista das bibliotecas do projeto está em um arquivo chamado **requirements.txt**. Instale as bibliotecas com o seguinte comando:
```
(venv) PS ...\export-comments-backend>pip install -r requirements.txt
```

4. Finalment, assim que todas as bibliotecas forem instaladas, você poderá rodar o backend do Orbit Export Comments:
```
(venv) PS ...\export-comments-backend>flask run
```







