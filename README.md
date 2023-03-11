# Crear un ambiente virtual y subir a Heroku. 
Esta demo, esta construida para la implementación de otras tecnologías y vincularlas con Salesforce utilizando Python como nuestro lenguaje backend junto con su micro framework llamado Flask( https://flask.palletsprojects.com ) para la creación de páginas web y Simple Salesforce( https://pypi.org/project/simple-salesforce ) , una api que nos permite trabajar con  datos de Salesforce.

<hr>

# Primero, debes descargar el repositorio y vincularlo con git. 
La siguiente aplicación cuenta con ajustes previos para ser utilizada en una aplicación de Heroku.

Si deseas crear un proyecto con lo mencionado anteriormente, debes realizar lo siguiente:

(Opcional) Instalar Flask y lo necesario en tu proyecto:
-	pip install flask
-	pip install simple-salesforce (Opcional si se trabaja con Salesforce)
-	pip install pandas (Opcional si se trabaja con Salesforce)

(Opcional) Crear un archivo llamado Procfile y lo guardamos sin formato. Después agregamos lo siguiente dentó del archivo:
-	gunicorn run:app

(Opcional) Crear un archivo runtime.txt y escribir lo siguiente en la terminal:
-	python –version

(Opcional) Luego copie dentro del archivo runtime.txt la versión que nos mostró el comando anterior con el formato python-x.x.x dentro del archivo. Por ejemplo:
-	python-3.9.5

<hr>

# Crear un ambiente Virtual
Después de crear tu aplicación en Python, Debes abrir una terminal desde la carpeta del proyecto y ejecutar en orden lo siguiente:
-	pip install virtualenv
-	python -m venv venv

Nos vamos al servidor a instalar siguiente (Debes instalar todo lo que instalaste en tu aplicación):
-	cd venv/Scripts
-	pip install flask
-	pip install simple-salesforce (Opcional si se trabaja con Salesforce)
-	pip install pandas (Opcional si se trabaja con Salesforce)
-	pip install gunicorn
-	python ../../run.py (Opcional)

Creación de los requerimientos que necesitara nuestro servidor Heroku desde la carpeta venv. Para crear el archivo escribimos el siguiente comando:
-	pip freeze > ../../requirements.txt
-   pip freeze > requirements.txt

Después de la creación, se debe eliminar dentro del archivo requirements.txt los siguientes requerimientos. Ya que, con estos archivos nos saldrá un error en la compilación de Heroku porque estamos instalando requerimientos de Windows en un servidor Linux.
-	pypiwin32==xxx 
-	pywin32==xxx

Para terminar, debes subir todo a git excepto la carpeta venv. Luego vas a Heroku, creas una aplicación https://dashboard.heroku.com/new-app y al crear tu aplicación vas a la pestaña Deploy, vinculas tu cuenta git y has un deploy de tu aplicación en la rama donde tengas tu codigo. Recuerda que la carpeta venv no va incluida en la rama master.

