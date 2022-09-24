FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install -r setup/requirements.txt

CMD ["python3", "pay_bot.py"]
