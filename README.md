# API-REST
# Docker Build Image
- docker build -t apirest:v1 .
# Docker Run
- docker run -it -v /workspace/API-REST/code:/home/code --net=host --name apirest -h mau apirest:v1

# Sql to Sqlite
- sqlite3 clientes.sqlite < clientes.sql

# Run Uvircorn
- uvicorn main:app

