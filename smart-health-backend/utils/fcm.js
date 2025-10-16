    const admin = require('firebase-admin');
    const serviceAccount = require('../mediware-714e0-firebase-adminsdk-fbsvc-55164465ec.json');

    admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    });

    const sendNotification = async (deviceToken, title, body) => {
    const message = {
        notification: { title, body },
        token: deviceToken,
    };

    try {
        const response = await admin.messaging().send(message);
        console.log('✅ Push notification sent:', response);
        return response;
    } catch (error) {
        console.error('❌ Error sending notification:', error);
        throw error;
    }
    };

    module.exports = sendNotification;
