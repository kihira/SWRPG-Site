FROM python:3.6-onbuild
ENV PYTHONUNBUFFERED 1

EXPOSE 5000:5000

CMD [ "gunicorn", "-b", ":5000", "-w", "2", "server:app" ]