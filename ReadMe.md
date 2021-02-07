# MY CRYPTO

    Aplicacion de simulacion de compra/venta de criptomonedas.

    Pasos a seguir para la instalación:

1. Crear entorno virtual (venv)

2. Instalar las dependencias:
    ```pip install -r requirements.txt```

3. Crear una base de datos:
    Entra en las carpetas proyecto/data y en el terminal escribe los comandos:
    ```
    > sqlite3 basededatos.db
    > .read migrations/initial.sql
    > .schema
    > .q
    ```

4. Crear variable de entorno, archivo **.env** con las siguientes variables:
    FLASK_APP=run.py
    FLASK_ENV=development

5. Crear un archivo **config.py** basado en config_template.py y reemplaza por las claves siguientes:
Clave secreta CSRF= 'crea una clave'
Ruta de la base de datos = 'proyecto/data/dbfile.db'
Clave de la API= 'obtenten una clave en https://coinmarketcap.com/api/'



### Finalmente arranca la aplicación



Notas: 
Esta aplicacion esta diseñada para Windows. 
Tienes que tener instalado Git y SQLITE3 en tu sistema.