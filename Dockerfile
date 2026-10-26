FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod -R g=u /app
EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_concert.wsgi:application"]
