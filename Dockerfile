FROM  python:3-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 main.py

EXPOSE 5000
