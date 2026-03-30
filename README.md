
# DevSecOps  

Aplicação Flask com uso de banco de dados, para demonstração de uma vulnerabilidade do tipo SQL Injection, identificável através de um SAST (Static Application Security Testing - Teste Estático de Segurança de Aplicação) especificado no arquivo .gitlab-ci.yml.

O DevSecOps integra práticas de segurança no fluxo de desenvolvimento e operações, promovendo a cultura de "segurança como disciplina". O objetivo é incorporar controles e verificações de segurança desde as primeiras etapas do desenvolvimento, utilizando ferramentas automatizadas para identificar vulnerabilidades em código, dependências e configurações. 

Esta abordagem garante que a segurança seja uma responsabilidade compartilhada entre todas as equipes, contribuindo para a entrega de software robusto e confiável sem comprometer a agilidade do pipeline DevOps.

## A Vulnerabilidade SQL Injection

- "Injections" são códigos maliciosos que podem ser inseridos das mais diversas formas em aplicações, como através de uma URL ou instrução SQL.
- Algumas abordagens para contorno:
    - Separar adequadamente comandos e dados dinâmicos, evitando uma concatenação direta de caracteres;
    - Uso de frameworks de apoio para construção e execução de instruções SQL.
  
## Código

    31    sql_Query_Not_Injection = text("SELECT * FROM users WHERE username=:username AND password=:password")
    32    result = conn.execute(sql_Query_Not_Injection, parameters=dict(username = username_from_form
    33                                                                   , password = password_from_form))
    34    
    35    sql_Query_Injection_False_Negative = text("SELECT * FROM users WHERE username = '" + username_from_form + "'"
    36                                           " AND password = " + password_from_form)                                         
    37    result = conn.execute(sql_Query_Injection_False_Negative)

    66 sql_Query_Not_Injection = text("select * from user where id=:user_id")
    67 result = conn.execute(sql_Query_Not_Injection, user_id = id)
    68
    69 sql_Query_Injection_False_Negative = text("SELECT * FROM users WHERE username = '" + username_from_url + "'"
    70                                      " AND password = " + password_from_url)                                         
    71 result = conn.execute(sql_Query_Injection_False_Negative)

 - As linhas 31, 32, 66 e 67 **não contém** uma vulnerabilidade SQL Injection;
 - As linhas 35, 36, 69 e 70 **contém** uma vulnerabilidade SQL Injection, **identificável**  no SAST do .gitlab-ci;

## Exercícios Propostos

1. **Explorar a vulnerabilidade de SQL Injection**

Via "GET":

Acessando a URL em seu navegador:

```
$ GET http://127.0.0.1:5000/login?username=%27%20or%201=1;%20--&password=1234
```

Via "POST":

Importando a collection flask-sql-injection.postman_collection.json no Postman
```
POST /login HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/x-www-form-urlencoded
Content-Length: 48

username='%20or%201%3D1%3B%20--%20&password=1234
```

2. **Corrigir a vulnerabilidade de SQL Injection, retomando a execução do pipeline com sucesso.**

## Executando a Aplicação

### Execução com docker compose, com MySQL
```
$ docker compose up -d
```

### Execução local, com SQLite
```
$ python app/app.py run
```

## mydb.db

|id|user |password|
|--|--|--|
|1 |teste@teste.com |1234|
|2 |teste2@teste.com |1234|
|3 |teste@teste.com |12345678|
|4 |teste2@teste.com |87654321|

Baseado no projeto [EstudosAvancadosSI](https://github.com/BrunoEleodoro/EstudosAvancadosSI)