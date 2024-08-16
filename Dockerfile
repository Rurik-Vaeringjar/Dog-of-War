FROM python:3
COPY requirements.txt ./
WORKDIR "/opt/dow"
COPY . .
RUN chmod +x bot.py && touch event.log
CMD ["python3", "./bot.py"]
