const express = require('express');
const multer = require('multer');
const path = require('path');
const { uploadPrescription } = require('../controllers/prescriptions.controllers');

const router = express.Router();

// Multer config
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, process.env.UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + '-' + file.originalname;
    cb(null, uniqueName);
  }
});
const upload = multer({ storage });

// Routes
router.get('/', (req, res) => {
  res.json({ message: 'Prescription route is working' });
});

router.post('/upload', upload.single('image'), uploadPrescription);

module.exports = router;
