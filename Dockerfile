FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

WORKDIR /app/
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt --prefer-binary --no-cache-dir

COPY . /app/

RUN mkdir -p data &&\
    python main.py setup-db &&\
    chmod -R 660 *

ENTRYPOINT ["python", "main.py"]
CMD ["serve"]

EXPOSE 8000
