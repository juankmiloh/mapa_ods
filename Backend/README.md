## Back-end para el manejo del módulo de procesos (expedientes) para la DIEG

# linux/MacOS
export FLASK_ENV=development
python3 manage.py runserver -h 0.0.0.0 -p 5000

# servidor SSPD
export FLASK_ENV=production
python3 app.py runserver -h 0.0.0.0 -p 5055

# Windows PowerShell revisar el archivo manage.py y escoger el ambiente a utilizar desarrollo o produccion
<!-- $env:FLASK_ENV = "production" -->
$env:FLASK_ENV = "development"
python app.py runserver -h 0.0.0.0 -p 5000

<!-- python3 manage.py runserver -h 0.0.0.0 -p 5000 -->