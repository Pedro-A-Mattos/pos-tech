# Tech Challenge

O objetivo deste projeto é desenvolver uma API pública que permita consultas automatizadas nos dados disponíveis no site [Vitivinicultura](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) para os tópicos de produção, processamento, comercialização, importação e exportação. A API será projetada para facilitar o acesso e a manipulação desses dados, permitindo que desenvolvedores e usuários possam integrar as informações em seus próprios sistemas ou realizar análises personalizadas.

## Instalação

### Instalação dos pacotes necessários

```
pip install -r requirements.txt
```

### Instalação do Google Chrome e Chromedriver

Para o correto funcionamento dos endpoints de Web Scraping se faz necessário a instalação do google chrome e chromedriver
[Download aqui](https://googlechromelabs.github.io/chrome-for-testing/)

## Testes

Para garantir que a aplicação funcionará corretamente você pode rodar os testes abaixo. Os testes visam não só garantir que o código está funcional, mas também validar a inicialização de componentes chaves como o chromedriver.

```bash
pytest src/tests/* -v
```

> Devido a oscilações no site da embrapa pode haver uma demora no teste "test_browser_automation.py::test_get_webdriver_valid_url".

## Rodando a aplicação

Para rodar o código localmente é necessário estar no diretório do projeto e execurar no terminal o seguinte comando

```
uvicorn src.main:app
```

O terminal retornará um link para acessar a API em `http://127.0.0.1:8000`. Adicionando /docs ao final da URL, como em `http://127.0.0.1:8000/docs`, você será redirecionado para a interface interativa do Swagger, onde poderá visualizar a documentação automática gerada para a API. Nesta interface, é possível explorar os endpoints disponíveis, testar as funcionalidades da API em tempo real e visualizar as respostas retornadas pelo servidor, tudo de maneira prática e intuitiva.

### Existem, ao todo, 5 endpoints disponíveis na API: tópicos, subtópicos, download, show, e user/login.

### 1. Autenticação (user/login):

Para acessar a primeira funcionalidade da API, é necessário primeiro autenticar-se. Utilize o endpoint user/login, fornecendo dados de login válidos que podem ser encontrados no arquivo src/auth/users.csv. Após o login bem-sucedido, será gerado um token JWT, que deve ser usado para autenticação nos demais endpoints.
Um exemplo de solicitação de login seria:

```
{
  "email": "user1@gmail.com",
  "password": "Teste1!"
}
```

Se o login for bem-sucedido, a API retornará um token JWT (JSON Web Token), que será necessário para autenticar sua requisição ao endpoint topicos.

```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidmlwZXJlaXJhQG1hcGZyZS5jb20uYnIiLCJleHBpcmVzIjoxNzIzMzI4MzM0LjY3MDkyMjh9.LLNb_dudDWBt34_PUswUn4C4q-bip_DQ5n_axneC_xA"
}
```

Esse token deve ser incluído no cabeçalho Authorization das requisições subsequente. Para fazer isso basta inserir o token na seção de autenticação.

![image](https://github.com/user-attachments/assets/a56d7fdd-aed7-4b19-9d98-1f5129211602)

### 2. Listagem de Tópicos (tópicos):

Após a autenticação, utilize o token JWT gerado para acessar o endpoint tópicos. Este endpoint retornará os links de cada tópico disponível (produção, processamento, comercialização, importação e exportação) no site.

```
{
  "Produção": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
  "Processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
  "Comercialização": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
  "Importação": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
  "Exportação": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
}
```

### 3. Listagem de Subtópicos (subtópicos):

Após obter os links dos tópicos, o próximo passo é utilizar o endpoint subtópicos. Este endpoint aceita os links dos tópicos como entrada e retorna os nomes dos arquivos CSV relacionados a cada tópico para download.

```
{
  "Produção": "Producao.csv",
  "Processamento": {
    "Viníferas": "ProcessaViniferas.csv",
    "Americanas e híbridas": "ProcessaAmericanas.csv",
    "Uvas de mesa": "ProcessaMesa.csv",
    "Sem classificação": "ProcessaSemclass.csv"
  },
  "Comercialização": "Comercio.csv",
  "Importação": {
    "Vinhos de mesa": "ImpVinhos.csv",
    "Espumantes": "ImpEspumantes.csv",
    "Uvas frescas": "ImpFrescas.csv",
    "Uvas passas": "ImpPassas.csv",
    "Suco de uva": "ImpSuco.csv"
  },
  "Exportação": {
    "Vinhos de mesa": "ExpVinho.csv",
    "Espumantes": "ExpEspumantes.csv",
    "Uvas frescas": "ExpUva.csv",
    "Suco de uva": "ExpSuco.csv"
  }
}
```

### 4. Download de Arquivos (download):

Para baixar os arquivos CSV, utilize o endpoint download. Forneça o nome do arquivo de um subtópico, e o arquivo será salvo na pasta storage do servidor.
Exemplo:

```
Producao.csv
```

### 5. Visualização de Arquivos (show):

Por fim, para verificar o conteúdo dos arquivos baixados, use o endpoint show. Ele aceita como entrada o nome do arquivo CSV e permite filtrar os dados por ano, facilitando a análise das informações.

### Documentação dos endpoints

Se preferir você pode consultar a [documentação da API disponível no Postman](https://documenter.getpostman.com/view/35378763/2sA3kd9ww1).

É possível executar as chamadas da API diretamente da documentação, e inclusive visualizar exemplos de código para a chamada da API em diferentes linguagens.

## Processo de Deploy da aplicação

Todos os detalhes do processo de deploy podem ser obtidos [aqui](deploy_documentation.md)
