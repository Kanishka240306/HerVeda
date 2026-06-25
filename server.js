const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const dns = require('dns').promises;

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'waitlist.json');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));

function isEmailSyntaxValid(email) {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
}

async function hasValidEmailDomain(domain) {
  try {
    const mxRecords = await dns.resolveMx(domain);
    if (Array.isArray(mxRecords) && mxRecords.length > 0) {
      return true;
    }
  } catch (mxError) {
    // no MX records, try A/AAAA lookup as fallback
  }

  try {
    const aRecords = await dns.resolve(domain);
    return Array.isArray(aRecords) && aRecords.length > 0;
  } catch (aError) {
    try {
      const aaaaRecords = await dns.resolve6(domain);
      return Array.isArray(aaaaRecords) && aaaaRecords.length > 0;
    } catch (aaaaError) {
      return false;
    }
  }
}

app.post('/waitlist', async (req, res) => {
  const { email } = req.body;
  const trimmedEmail = typeof email === 'string' ? email.trim().toLowerCase() : '';

  if (!trimmedEmail) {
    return res.status(400).json({ success: false, message: 'Please enter your email address.' });
  }

  if (!isEmailSyntaxValid(trimmedEmail)) {
    return res.status(400).json({ success: false, message: 'Please enter a valid email address.' });
  }

  const domain = trimmedEmail.split('@')[1];
  if (!domain) {
    return res.status(400).json({ success: false, message: 'Please enter a valid email address.' });
  }

  const domainExists = await hasValidEmailDomain(domain);
  if (!domainExists) {
    return res.status(400).json({ success: false, message: 'Email domain does not appear to be valid.' });
  }

  let waitlist = [];

  try {
    const content = await fs.readFile(DATA_FILE, 'utf8');
    waitlist = JSON.parse(content);
    if (!Array.isArray(waitlist)) {
      waitlist = [];
    }
  } catch (error) {
    if (error.code !== 'ENOENT') {
      console.error('Unable to read waitlist file:', error);
      return res.status(500).json({ success: false, message: 'Server error reading data.' });
    }
  }

  if (waitlist.some((entry) => entry.email === trimmedEmail)) {
    return res.status(409).json({ success: false, message: 'This email is already on the waitlist.' });
  }

  const entry = {
    email: trimmedEmail,
    createdAt: new Date().toISOString(),
  };

  waitlist.push(entry);

  try {
    await fs.writeFile(DATA_FILE, JSON.stringify(waitlist, null, 2), 'utf8');
  } catch (error) {
    console.error('Unable to save waitlist entry:', error);
    return res.status(500).json({ success: false, message: 'Server error saving data.' });
  }

  return res.json({ success: true, message: 'Thank you! We will be in touch soon.' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'Herveda backend' });
});

app.listen(PORT, () => {
  console.log(`Herveda backend running at http://localhost:${PORT}`);
});
