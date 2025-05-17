FROM python:3.11-slim

WORKDIR /{{ project_name }}

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "manage.py"]
