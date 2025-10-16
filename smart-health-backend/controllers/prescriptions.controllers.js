const Tesseract = require('tesseract.js');
const path = require('path');
const { spawn } = require('child_process');
const notificationQueue = require('../queues/notificationQueue');



// Helper function to clean JSON response from markdown
function cleanJsonResponse(text) {
  // Remove markdown code blocks
  let cleaned = text.replace(/```json\s*/g, '').replace(/```\s*/g, '');
  // Remove any extra whitespace and line breaks
  cleaned = cleaned.trim();
  return cleaned;
}

const uploadPrescription = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const filename = req.file.filename;
    const filepath = path.join('uploads', filename);
    const fullPath = path.join(__dirname, '..', 'uploads', filename);

    // OCR with Tesseract
    console.log('Starting OCR processing...');
    const { data: { text } } = await Tesseract.recognize(fullPath, 'eng');
    console.log('OCR completed, extracted text:', text);

    // Process with Gemini Python script
    const python = spawn('python', [path.join(__dirname, '..', 'gemini.py')]);
    let resultData = '';
    let errorData = '';

    python.stdin.write(text);
    python.stdin.end();

    python.stdout.on('data', (data) => {
      resultData += data.toString();
    });

    python.stderr.on('data', (err) => {
      errorData += err.toString();
      console.error('Gemini Python error:', err.toString());
    });

    python.on('close', (code) => {
      if (code !== 0) {
        console.error('Python script failed with code:', code);
        console.error('Error output:', errorData);
        return res.status(500).json({ 
          error: 'Gemini script execution failed', 
          code: code,
          stderr: errorData 
        });
      }

      try {
        const cleanedData = cleanJsonResponse(resultData);
        console.log('Cleaned response:', cleanedData);
        const parsed = JSON.parse(cleanedData);
        scheduleNotifications(parsed);
        return res.status(200).json({
          message: 'Prescription uploaded and processed successfully',
          filename,
          filepath,
          extractedText: text,
          geminiExtracted: parsed
        });
        function getTimeSlots(frequency) {
          const TIME_SLOTS = ['08:00', '13:00', '20:00'];
          return frequency.split('-')
            .map((val, i) => (val === '1' ? TIME_SLOTS[i] : null))
            .filter(Boolean);
        }

        function scheduleNotifications(meds) {
          const now = new Date();

          meds.forEach(({ medicine, frequency, days }) => {
            const timeSlots = getTimeSlots(frequency);
            const dosesPerDay = timeSlots.length;

            for (let d = 0; d < days; d++) {
              timeSlots.forEach(timeStr => {
                const [h, m] = timeStr.split(':');
                const notifyAt = new Date(now);
                notifyAt.setDate(now.getDate() + d);
                notifyAt.setHours(parseInt(h), parseInt(m), 0);

                const delay = notifyAt - new Date();

                notificationQueue.add({
                  type: 'dose',
                  medicine,
                  notifyAt
                }, { delay });
                // Log the scheduled dose reminder
                console.log(`Scheduled dose reminder for ${medicine} at ${notifyAt.toISOString()}`);
              });
            }

            // Refill reminder
            const refillAt = new Date(now);
            refillAt.setDate(refillAt.getDate() + days);
            refillAt.setHours(9, 0, 0);

            const delay = refillAt - new Date();

            notificationQueue.add({
              type: 'refill',
              medicine,
              notifyAt: refillAt,
              quantity: dosesPerDay * days
            }, { delay });
            // Log the scheduled notifications
            console.log(`Scheduled notifications for ${medicine}:`, {
              doses: days * dosesPerDay,
              refillAt: refillAt.toISOString()
            });
          });
        }



      } catch (e) {
        console.error('Failed to parse Gemini response:', e.message);
        console.error('Raw response:', resultData);
        console.error('Cleaned response:', cleanJsonResponse(resultData));
        return res.status(500).json({ 
          error: 'Failed to parse Gemini response', 
          raw: resultData,
          cleaned: cleanJsonResponse(resultData),
          parseError: e.message 
        });
      }
    });

  } catch (error) {
    console.error('Controller error:', error);
    return res.status(500).json({ error: 'Internal server error', details: error.message });
  }
};

module.exports = {
  uploadPrescription
};
