# GUIA DE USO
## Inicia un entorno virtual
~~~
python3 -m venv .venv
~~~
## Instala los paquetes necesarios
~~~
pip install -r requeriments.txt
~~~
##crea un archivo .env en la raiz del proyecto, estructurado de la siguiente forma
~~~
DB_USER='tu usario de base de datos'
DB_PASSWORD='tu contraseña de la base de datos'
DB_HOST='el host'
DB_PORT='el puerto por el que se comunica la base de datos'
DB_NAME='nombre de la base de datos'
~~~
Esto con el fin de establecer la conexion a la base de datos por medio de
~~~
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
~~~
##ejecución del programa
~~~
python app.py
~~~
# IMPORTANTE
- Solo necesitas crear la base de datos, no las tablas, ya que estas se generan automaticamente con la ejecucion de ***python app.py***
- Antes de hacer un POST a la tabla 'materia_prima_producto' en la ruta '/descontar_mp' debes hacer un POST en la ruta '/asociar_mp' para que cree la relacion de la materia prima
con el producto y a su vez la cantidad de materia prima a descontar
- Usar **Postman** o cualquier otra herramienta como **Insomnia**, **Hoppscotch**, entre otros, para testear.
