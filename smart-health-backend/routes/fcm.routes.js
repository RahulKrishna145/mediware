const express = require('express');
const { registerToken } = require('../controllers/fcmtoken.controllers');
const router = express.Router();

router.post('/register-token', registerToken);

module.exports = router;
