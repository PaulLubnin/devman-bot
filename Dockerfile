FROM python:3.10
COPY requirements.txt /opt/devman-bot/requirements.txt
WORKDIR /opt/devman-bot
RUN pip install -r requirements.txt
COPY . /opt/devman-bot
CMD ["python", "./main.py"]
