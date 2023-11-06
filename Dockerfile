FROM python:3
ADD smartcart.py .
COPY . /Tubes-TST-API
WORKDIR /Tubes-TST-API
RUN pip install fastapi uvicorn mysql.connector.python
CMD [ "uvicorn", "smartcart:app", "--host=0.0.0.0", "--port=80" ]