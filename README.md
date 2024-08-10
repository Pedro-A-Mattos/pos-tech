# Tech Challenge

O objetivo deste projeto é desenvolver uma API pública que permita consultas automatizadas nos dados disponíveis no site [Vitivinicultura](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) para os tópicos de produção, processamento, comercialização, importação e exportação. A API será projetada para facilitar o acesso e a manipulação desses dados, permitindo que desenvolvedores e usuários possam integrar as informações em seus próprios sistemas ou realizar análises personalizadas. 

Intalação dos pacotes necessários
````
pip install -r requirements.txt
````

Para rodar o código localmente é necessário estar no diretório do projeto e execurar no terminal o seguinte comando
````
uvicorn src.main:app
````

O terminal retornará um link para acessar a API em ``http://127.0.0.1:8000``. Adicionando /docs ao final da URL, como em ``http://127.0.0.1:8000/docs``, você será redirecionado para a interface interativa do Swagger, onde poderá visualizar a documentação automática gerada para a API. Nesta interface, é possível explorar os endpoints disponíveis, testar as funcionalidades da API em tempo real e visualizar as respostas retornadas pelo servidor, tudo de maneira prática e intuitiva.
 
# Existem, ao todo, 5 endpoints disponíveis na API: tópicos, subtópicos, download, show, e user/login.

## 1. Autenticação (user/login):

Para acessar a primeira funcionalidade da API, é necessário primeiro autenticar-se. Utilize o endpoint user/login, fornecendo dados de login válidos que podem ser encontrados no arquivo src/auth/users.csv. Após o login bem-sucedido, será gerado um token JWT, que deve ser usado para autenticação nos demais endpoints.
Um exemplo de solicitação de login seria:
````
{
  "email": "vipereira@mapfre.com.br",
  "password": "Teste1!"
}
````

Se o login for bem-sucedido, a API retornará um token JWT (JSON Web Token), que será necessário para autenticar sua requisição ao endpoint topicos. 
````
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidmlwZXJlaXJhQG1hcGZyZS5jb20uYnIiLCJleHBpcmVzIjoxNzIzMzI4MzM0LjY3MDkyMjh9.LLNb_dudDWBt34_PUswUn4C4q-bip_DQ5n_axneC_xA"
}
````

Esse token deve ser incluído no cabeçalho Authorization das requisições subsequente. Para fazer isso basta inserir o token na seção de autenticação.

![image](https://github.com/user-attachments/assets/a56d7fdd-aed7-4b19-9d98-1f5129211602)


## 2. Listagem de Tópicos (tópicos):

Após a autenticação, utilize o token JWT gerado para acessar o endpoint tópicos. Este endpoint retornará os links de cada tópico disponível (produção, processamento, comercialização, importação e exportação) no site.

## 3. Listagem de Subtópicos (subtópicos):
Com os links dos tópicos em mãos, o próximo passo é utilizar o endpoint subtópicos, que aceita como entrada o link de um tópico e retorna os links de download dos arquivos CSV relacionados a esse tópico.

## 4. Download de Arquivos (download):
Para baixar os arquivos CSV, utilize o endpoint download. Forneça o link de download de um subtópico, e o arquivo será salvo na pasta storage do servidor.

## 5. Visualização de Arquivos (show):

Por fim, para verificar o conteúdo dos arquivos baixados, use o endpoint show. Ele aceita como entrada o nome do arquivo CSV e permite filtrar os dados por ano, facilitando a análise das informações.

 
 # running tests

from pos-tech

```bash
pytest src/tests/<file_name>
```
