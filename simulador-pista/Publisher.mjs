import mqtt from 'mqtt';

export default class Publisher {
  constructor(brokerUrl = 'mqtt://localhost:1883') {
    this.client = mqtt.connect(brokerUrl);

    this.client.on('connect', () => {
      console.log(`Connected to MQTT broker at ${brokerUrl}`);
    });

    this.client.on('error', (error) => {
      console.error(`MQTT connection error: ${error}`);
    });
  }

  publish(topic, message) {
    this.client.publish(topic, message, (error) => {
      if (error) {
        console.error(`Publish error: ${error}`);
      } else {
        console.log(`Message published to ${this.topic}: ${message}`);
      }
    });
  }

  disconnect() {
    this.client.end(() => {
      console.log('Disconnected from MQTT broker');
    });
  }
}