FROM fedora:38
COPY requirements.txt requirements.txt
RUN dnf -y install python3 && dnf -y install python3-pip && pip install -r requirements.txt
WORKDIR "/opt/dow"
COPY . .
RUN chmod +x bot.py && touch event.log
CMD ["python3", "./bot.py"]
