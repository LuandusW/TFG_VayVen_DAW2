# Base de datos
Para este proyecto estoy utilizando Postgres
https://www.postgresql.org/

# Dependiendo de como tengas instalado python en su local puede ser python -m venv .venv u python3 en mac

# Instalar .Env
py -m venv .env

# Activar entorno .Env
source .env/Scripts/activate

# Instalar dependencias 
pip install -r requirements.txt
# Instalar las librerías necesarias para ejecutar el proyecto 
py -m pip install flask-sqlalchemy 
py -m pip install bcrypt 
py -m pip install psycopg2-binary 
py -m pip install python-dotenv
py -m pip install flask-mail
