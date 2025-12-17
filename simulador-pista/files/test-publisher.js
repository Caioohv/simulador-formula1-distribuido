import Publisher from '../Publisher.mjs';

const publisher = new Publisher('mqtt://localhost:1883', 'test-topic');

setTimeout(() => {
  publisher.publish('Hello, MQTT!');
}, 1000);