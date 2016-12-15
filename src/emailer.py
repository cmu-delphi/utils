"""
===============
=== Purpose ===
===============

A program used for sending emails through Automation.


=================
=== Changelog ===
=================

2016-12-14
  + more secrets
2016-12-12
  + use secrets
  * checking in existing version
"""

import mysql.connector
import argparse
import requests
import base64
import json
import secrets

#Functions to encode and decode messages
def encode(x):
  return 'b64|%s'%(base64.b64encode(json.dumps(x).encode('utf-8')).decode("utf-8"))
def decode(x):
  return json.loads(base64.b64decode(x[4:].encode('utf-8')).decode("utf-8"))

#Connect to the database as the automation user
def _connect():
  u, p = secrets.db.auto
  return mysql.connector.connect(user=u, password=p, database='automation')

#Add an email to the database queue
def queue_email(to, subject, text, cc=None, bcc=None, html=None, attachments=None):
  #Build the body data string
  data = {'text': text}
  if cc is not None:
    data['cc'] = cc
  if bcc is not None:
    data['bcc'] = bcc
  if html is not None:
    data['html'] = html
  if attachments is not None:
    data['attachments'] = attachments
  body = encode(data)
  if len(body) >= 16384:
    raise Exception('Encoded email overflows database field (max=16383|len=%d)'%(len(body)))
  #Connect, queue, commit, and disconnect
  cnx = _connect()
  cur = cnx.cursor()
  cur.execute("INSERT INTO email_queue (`from`, `to`, `subject`, `body`) VALUES ('%s','%s','%s','%s')"%(secrets.flucontest.email_epicast, to, subject, body))
  cnx.commit()
  cur.close()
  cnx.close()

#Add an email to the database queue
def call_emailer():
  #Connect, call, and disconnect
  cnx = _connect()
  cur = cnx.cursor()
  cur.execute("CALL RunStep(2)")
  cnx.commit()
  cur.close()
  cnx.close()

#Function to send email with the mailgun API
def _send_email(frm, to, subject, body):
  auth = ('api', secrets.mailgun.key)
  files = None
  data = {
    'from': frm,
    'to': to,
    'subject': subject,
  }
  #The body is either plain text or a base64 encoded JSON string
  if body[:4] == 'b64|':
    x = decode(body)
    if 'text' not in x:
      raise Exception('Field \'text\' is missing')
    data['text'] = x['text']
    if 'html' in x:
      data['html'] = x['html']
    if 'cc' in x:
      data['cc'] = x['cc']
    if 'bcc' in x:
      data['bcc'] = x['bcc']
    if 'attachments' in x:
      files = []
      for attachment in x['attachments']:
        #Each attachment is (file_name, mime_type)
        if type(attachment[0]) in (list, tuple):
          attachment = attachment[0]
        files.append(('attachment', (attachment[0], open(attachment[0], 'rb'), attachment[1])))
  else:
    data['text'] = body
  try:
    print('Sending email: %s -> %s "%s"'%(frm, to, subject))
    r = requests.post('https://api.mailgun.net/v2/epicast.net/messages', auth=auth, data=data, files=files)
    return (r.status_code == 200) and (r.json()['message'] == 'Queued. Thank you.')
  except Exception:
    return False

if __name__ == '__main__':
  #Args and usage
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False, help="show extra output")
  parser.add_argument('-t', '--test', action='store_const', const=True, default=False, help="test run only, don't send emails or update the database")
  args = parser.parse_args()

  #DB connection
  if args.verbose: print('Connecting to the database')
  cnx = _connect()
  select = cnx.cursor()
  update = cnx.cursor()
  if args.verbose: print('Connected successfully')

  #Get the list of emails
  select.execute('SELECT `id`, `from`, `to`, `subject`, `body` FROM `email_queue` WHERE `status` = 0')
  emails = []
  for (email_id, email_from, email_to, email_subject, email_body) in select:
    emails.append({
      "id": email_id,
      "from": email_from,
      "to": email_to,
      "subject": email_subject,
      "body": email_body,
    })
  if args.verbose: print('Found %d email(s)'%(len(emails)))

  #Send emails
  for email in emails:
    if args.verbose: print(' [%s] %s -> %s "%s" (%d)'%(email['id'], email['from'], email['to'], email['subject'], len(email['body'])))
    if args.test: continue
    #Sending in progress
    update.execute('UPDATE email_queue SET status = 2 WHERE id = %s'%(email['id']))
    cnx.commit()
    #Send
    success = _send_email(email['from'], email['to'], email['subject'], email['body'])
    #Success or failure
    if success:
      if args.verbose: print(' Success')
      update.execute('UPDATE email_queue SET status = 1 WHERE id = %s'%(email['id']))
    else:
      if args.verbose: print(' Failure')
      update.execute('UPDATE email_queue SET status = 3 WHERE id = %s'%(email['id']))
    cnx.commit()

  #Cleanup
  cnx.commit()
  select.close()
  update.close()
  cnx.close()
