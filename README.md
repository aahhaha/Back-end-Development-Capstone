# Back-end-Development-Capstone

Djirection band website, based on the official IBM capstone template.
Django integrates the Songs Flask/MongoDB API and Pictures Flask API.

## Environment Setup
Python 3.12. Install `requirements.txt` in an activated virtual environment.
The original Cloud IDE setup script remains in `bin/setup.sh`.

Set SONGS_SERVICE_URL and PICTURES_SERVICE_URL (defaults http://127.0.0.1:8080 and http://127.0.0.1:8081).

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Home, Songs (lyrics modal), Photos, Concerts, signup/login and concert attendance are implemented.
Create concerts through Django admin. Run `python manage.py test` for page/integration/attendance checks.
Photo and Song are unmanaged representations of the external service resources.

## Deployment
Build with `docker build -t django-capstone .`.
Set DJANGO_SECRET_KEY, DJANGO_DEBUG=0, DJANGO_ALLOWED_HOSTS, SONGS_SERVICE_URL and PICTURES_SERVICE_URL for deployment.
Static files are served with WhiteNoise. The entrypoint applies committed migrations and collects static files.
Use `deployment.yml` after setting its container image and service environment values for your cluster.
SQLite is for the single-replica teaching deployment; use persistent storage or a managed database for durable production data.
