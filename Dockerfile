FROM python:3.12

RUN mkdir /app

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]