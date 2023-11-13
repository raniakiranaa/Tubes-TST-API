FROM python:3
WORKDIR /Tubes-TST-API
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD [ "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80" ]