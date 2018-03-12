FROM node:9.8 as builder
WORKDIR /usr/src/build

COPY package*.json ./
RUN npm install --production

COPY assets ./assets
COPY tsconfig.json ./
RUN mkdir -p ./static/img
RUN npm run build


FROM python:3.6
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server ./server
COPY static ./static
COPY --from=builder /usr/src/build/static ./static

ENV PYTHONUNBUFFERED 1
ENV DB_CONN "mongodb://localhost:27017"
EXPOSE 8000

CMD [ "gunicorn", "-b", ":8000", "-w", "2", "server:app" ]