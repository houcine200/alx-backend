// Import necessary modules from the redis package
import { createClient } from 'redis';

const subscriber = createClient();

subscriber.on('connect', function() {
  console.log('Redis client connected to the server');
});

subscriber.on('error', function (err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Subscribe to the channel 'holberton school channel'
subscriber.subscribe('holberton school channel');

// Handle incoming messages on the subscribed channel
subscriber.on('message', function (channel, message) {
  console.log(message);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe('holberton school channel');
    subscriber.quit();
  }
});
