# API-REST
# Docker Build Image
- docker build -t apirest:v1 .

# Docker Run
- docker run -it -v /workspace/API-REST/apirest:/home/apirest --net=host --name apirest -h mau apirest:v1

# Sql to Sqlite
- sqlite3 clientes.sqlite < clientes.sql
- sqlite3 usuarios.sqlite < usuarios.sql

# Run Uvircorn
- uvicorn main:app

# __init__.py necessary to execute pytest

# Run pytest
- python3 -m pytest -v

# Uvicorn option 2 
- uvicorn code.main:app