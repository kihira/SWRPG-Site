FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONUNBUFFERED 1

CMD [ "gunicorn", "-b", ":8000", "-w", "2", "server:app" ]
