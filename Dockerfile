FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# here i think that command should be COPY app/. Because the app.py is inside the app folder
#to build image in contaienr we use docker build -t filename-flask
COPY app/ .       

EXPOSE 5000

CMD ["python", "app.py"]
