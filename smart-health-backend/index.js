const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const prescriptionRoutes = require('./routes/prescriptions.routes');
const fcmRoutes = require('./routes/fcm.routes');


dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());
//fiebase cloud messaging token verification
app.use('/fcm', fcmRoutes);
// Serve static files from uploads/
app.use('/uploads', express.static(process.env.UPLOAD_DIR));

// Routes
app.get('/', (req, res) => {
    res.json({ message: 'Welcome to the Smart Health Backend API' });
    });
app.use('/api/prescriptions', prescriptionRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
