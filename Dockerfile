FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN pip install -i https://test.pypi.org/simple/ my-krml-24587139

COPY ./app /app

COPY ./models /models

COPY ./src /src

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "main:app"]