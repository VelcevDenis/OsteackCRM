FROM python:3.13.0-slim
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
COPY . .

CMD [ "python" , "main.py" ]