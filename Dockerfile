FROM python3.9
WORKDIR /app
COPY requirements.txt requirements.txt
COPY main.py main.py
RUN pip3 install -r requirements.txt
CMD [ "python3", "main.py"]