FROM python:3.12
WORKDIR /code

COPY ./users/ /code
COPY ./models/ /code/models
COPY ./utils/ /code/utils
COPY ./requirements.txt /code
RUN pip install -r /code/requirements.txt

ENTRYPOINT ["bash", "-c", "uvicorn main:app --port 8080 --host 0.0.0.0"]
