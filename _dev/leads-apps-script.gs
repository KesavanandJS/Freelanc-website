/* Google Apps Script — logs contact-form leads from the website into this Sheet,
 * then emails the admin so new leads aren't missed.
 *
 * Setup:
 * 1. Create a new Google Sheet (any name).
 * 2. Extensions -> Apps Script. Delete the default code and paste this file's contents.
 * 3. Set ADMIN_EMAIL below to where new-lead notifications should go.
 * 4. Deploy -> New deployment -> type "Web app".
 *    Execute as: Me. Who has access: Anyone.
 * 5. Copy the Web app URL (ends in /exec).
 * 6. Paste it into GOOGLE_SHEET_WEBHOOK in _dev/layout.py, then run: python _dev/build.py
 *
 * Each submission appends a row to the "Leads" tab (created automatically on first run)
 * and sends ADMIN_EMAIL a short notification email with the same details.
 */
var ADMIN_EMAIL = 'hello@pixelloom.in'; // change to the inbox that should get new-lead alerts

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Leads');
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Leads');
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Timestamp', 'Name', 'Phone', 'Business', 'Website type', 'Budget', 'Message']);
  }
  var p = e.parameter || {};
  var lead = {
    name: p.name || '',
    phone: p.phone || '',
    business: p.business || '',
    type: p.type || '',
    budget: p.budget || '',
    message: p.message || '-'
  };
  sheet.appendRow([new Date(), lead.name, lead.phone, lead.business, lead.type, lead.budget, lead.message]);
  notifyAdmin(lead);
  return ContentService.createTextOutput(JSON.stringify({ result: 'success' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function notifyAdmin(lead) {
  if (!ADMIN_EMAIL) return;
  var subject = 'New website enquiry: ' + lead.name + ' (' + lead.business + ')';
  var body = 'New quote request from the website:\n\n' +
    'Name: ' + lead.name + '\n' +
    'Phone: ' + lead.phone + '\n' +
    'Business: ' + lead.business + '\n' +
    'Website type: ' + lead.type + '\n' +
    'Budget: ' + lead.budget + '\n' +
    'Message: ' + lead.message;
  try {
    MailApp.sendEmail(ADMIN_EMAIL, subject, body);
  } catch (err) {
    // A failed email should never break the lead being saved to the Sheet.
  }
}
