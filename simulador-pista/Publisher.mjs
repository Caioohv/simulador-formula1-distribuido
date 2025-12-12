import mqtt from 'mqtt';

export default class Publisher {
  constructor(brokerUrl, topic) {
    this.client = mqtt.connect(brokerUrl);
    this.topic = topic;

    this.client.on('connect', () => {
      console.log(`Connected to MQTT broker at ${brokerUrl}`);
    });

    this.client.on('error', (error) => {
      console.error(`MQTT connection error: ${error}`);
    });
  }

  publish(message) {
    this.client.publish(this.topic, message, (error) => {
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