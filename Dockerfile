FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .

RUN touch README.md

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir build 
RUN pip install --no-cache-dir .

COPY . .

RUN python manage.py migrate 

CMD ["gunicorn", "task_manager.wsgi:application", "--bind", "0.0.0.0:8000"]