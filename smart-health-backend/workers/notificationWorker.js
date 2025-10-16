// workers/notificationWorker.js
const notificationQueue = require('../queues/notificationQueue');
const sendNotification = require('../utils/fcm');
const { DateTime } = require('luxon');

// For now, mock a device token
const { getTokens } = require('../controllers/fcmToken.controller');
const deviceTokens = getTokens();

for (const token of deviceTokens) {
  await sendNotification(token, title, body);
}

notificationQueue.process(async (job) => {
  const { type, medicine, notifyAt, quantity } = job.data;

  const nowIST = DateTime.now().setZone('Asia/Kolkata').toFormat('yyyy-MM-dd HH:mm:ss');
  const notifyAtIST = DateTime.fromISO(notifyAt, { zone: 'utc' }).setZone('Asia/Kolkata').toFormat('yyyy-MM-dd HH:mm:ss');

  let title, body;

  if (type === 'dose') {
    title = `Time to take ${medicine}`;
    body = `As per your schedule: ${notifyAtIST} IST`;
  } else if (type === 'refill') {
    title = `Refill Reminder for ${medicine}`;
    body = `You need ${quantity} more doses.`;
  } else {
    return 'Unknown notification type';
  }

  console.log(`🔔 [${nowIST}] Sending push: ${title} - ${body}`);

  await sendNotification(mockDeviceToken, title, body);

  return `Push sent for ${medicine}`;
});
