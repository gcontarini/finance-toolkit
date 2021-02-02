FROM python:3.8-slim

WORKDIR /finance-toolkit

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 -m unittest discover -s tests/ -p '*_test.py'