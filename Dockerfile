FROM python:3.6-onbuild
ENV PYTHONUNBUFFERED 1

CMD [ "gunicorn", "-b", ":8000", "-w", "2", "server:app" ]