#!/usr/bin/env node
/**
 * Lark Calendar Range Fetcher — SEONGON
 * Usage: node fetch_calendar_range.js <startISO> <endISO>
 * Example: node fetch_calendar_range.js 2026-05-11T00:00:00+07:00 2026-05-18T23:59:59+07:00
 * Output: JSON to stdout
 */

const keytar = require(require('os').homedir() + '/.lark-mcp/node_modules/keytar');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const https = require('https');
const zlib = require('zlib');

const STORAGE_FILE = path.join(
  process.env.HOME,
  'Library/Application Support/lark-mcp-nodejs/storage.json'
);
const CAL_ID = 'feishu.cn_OslXluYRNofZNW5MMxdUth@group.calendar.feishu.cn';

// ── HTTP helper ───────────────────────────────────────────────────────────────
function request(method, urlPath, token, body) {
  return new Promise((resolve, reject) => {
    const u = new URL('https://open.larksuite.com' + urlPath);
    const opts = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
      },
    };
    const req = https.request(opts, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        const enc = res.headers['content-encoding'];
        const decompress = enc === 'gzip' ? zlib.gunzip
          : enc === 'deflate' ? zlib.inflate
          : (b, cb) => cb(null, b);
        decompress(buf, (err, result) => {
          if (err) return reject(err);
          try { resolve(JSON.parse(result.toString('utf8'))); }
          catch { resolve({ raw: result.toString('utf8').slice(0, 500) }); }
        });
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ── Auth ──────────────────────────────────────────────────────────────────────
async function getUAT() {
  const aesKey = await keytar.getPassword('lark-mcp', 'encryption-key');
  if (!aesKey) throw new Error('No lark-mcp key. Run: lark-mcp login');
  const raw = fs.readFileSync(STORAGE_FILE, 'utf8');
  const [ivHex, encrypted] = raw.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const key = Buffer.from(aesKey, 'hex');
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  let dec = decipher.update(encrypted, 'hex', 'utf8');
  dec += decipher.final('utf8');
  const storage = JSON.parse(dec);
  const entry = Object.values(storage.tokens || {})[0];
  if (!entry) throw new Error('No token stored. Run: lark-mcp login');
  return entry.token;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const startArg = process.argv[2];
  const endArg   = process.argv[3];
  if (!startArg || !endArg) {
    console.error('Usage: node fetch_calendar_range.js <startISO> <endISO>');
    process.exit(1);
  }

  const startTs = Math.floor(new Date(startArg).getTime() / 1000);
  const endTs   = Math.floor(new Date(endArg).getTime()   / 1000);

  const uat = await getUAT();

  const res = await request(
    'GET',
    `/open-apis/calendar/v4/calendars/${encodeURIComponent(CAL_ID)}` +
    `/events?start_time=${startTs}&end_time=${endTs}&page_size=50`,
    uat
  );

  if (res.code !== 0) {
    console.error(JSON.stringify({ error: res.msg, code: res.code }));
    process.exit(1);
  }

  // Chỉ trả về confirmed events, map ra các trường cần thiết
  const items = (res.data.items || [])
    .filter(e => e.status === 'confirmed')
    .map(e => ({
      id:          e.event_id,
      summary:     e.summary || '(no title)',
      start:       e.start_time,
      end:         e.end_time,
      description: (e.description || '').trim(),
      recurrence:  e.recurrence || '',
      is_exception: e.is_exception || false,
      organizer:   e.event_organizer?.display_name || '',
      self_rsvp:   e.self_rsvp_status || 'none',
      vchat:       e.vchat?.meeting_url || '',
    }));

  console.log(JSON.stringify({ startTs, endTs, total: items.length, items }, null, 2));
}

main().catch(e => {
  console.error(JSON.stringify({ error: e.message }));
  process.exit(1);
});
