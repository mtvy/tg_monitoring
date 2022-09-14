FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN python3 database.py -c -l

CMD ["python3", "bot.py"]