FROM node:10 as builder
WORKDIR /usr/src/build

COPY package.json yarn.lock ./
RUN yarn install --production

COPY assets ./assets
COPY tsconfig.json build.js ./
RUN yarn run build


FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server ./server
#COPY static ./static
COPY users.json ./
COPY --from=builder /usr/src/build/static ./static

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP "server"
ENV DB_CONN "mongodb://localhost:27017"
EXPOSE 8000

CMD [ "gunicorn", "-b", ":8000", "-w", "2", "server:app" ]