// queues/notificationQueue.js
const Queue = require('bull');

const notificationQueue = new Queue('medication-reminders', {
  redis: { host: '127.0.0.1', port: 6379 }
});

notificationQueue.on('waiting', (jobId) => {
  console.log(`🕓 Job waiting in queue: ${jobId}`);
});

notificationQueue.on('active', (job) => {
  console.log(`⚙️  Job started:`, job.id, job.data);
});

notificationQueue.on('completed', (job, result) => {
  console.log(`✅ Job completed:`, job.id, 'Result:', result);
});

notificationQueue.on('failed', (job, err) => {
  console.error(`❌ Job failed:`, job.id, 'Error:', err);
});

module.exports = notificationQueue;
