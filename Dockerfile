FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install -r setup/requirements.txt

RUN python3 back/database.py -d -c

CMD ["python3", "bot.py"]

