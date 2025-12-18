FROM node:20-alpine

WORKDIR /home/viier/projects/ifmg/sd/formula1/simulador-pista

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

ENV MQTT_URL=localhost:1883

CMD ["node", "index.mjs"]
