FROM python:3.8

RUN apt-get update

WORKDIR /dados

COPY . /dados

RUN chmod -R 666 /dados

RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["python", "src/main.py"]