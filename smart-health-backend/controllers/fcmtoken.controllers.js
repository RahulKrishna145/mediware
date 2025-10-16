let deviceTokens = []; // temporary in-memory store

const registerToken = (req, res) => {
  const { token } = req.body;

  if (!token) {
    return res.status(400).json({ error: 'No token provided' });
  }

  // Avoid duplicates
  if (!deviceTokens.includes(token)) {
    deviceTokens.push(token);
    console.log('✅ Registered token:', token);
  }

  res.status(200).json({ message: 'Token registered successfully' });
};

const getTokens = () => deviceTokens;

module.exports = { registerToken, getTokens };
