FROM python:3.13-slim

WORKDIR /app

# instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copia código
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]