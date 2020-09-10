import imaplib
import email
import datetime

server = 'outlook.office365.com'
user = 'judemolloybusiness@outlook.com'
password = 'Test12345'

mailbox = 'Inbox'


def IMAP_fetch_emails(server, user, password):
    # Create the connection
    imap = imaplib.IMAP4_SSL(server)
    imap.login(user, password)

    # Select the mailbox
    email_count = imap.select(mailbox, True)

    # Calculate the date 45 days ago.
    start_date = '{:%d-%b-%Y}'.format(datetime.datetime.now() + datetime.timedelta(-1))

    messages = imap.search(None, '(SINCE "{}")'.format(start_date))

    print('The inbox has {} emails.'.format(email_count))

    resp, items = imap.search(None, '(SINCE "{}")'.format(start_date))

    for n, num in enumerate(items[0].split(), 1):
        resp, data = imap.fetch(num, '(RFC822)')

        body = data[0][1]
        msg = email.message_from_bytes(body)
        from_var = msg['from']
        content = msg.get_payload()


        print("=======================================================================================================")
        print("=======================================================================================================")
        print("=======================================================================================================")

        print(from_var)
        print(msg['subject'])
        print(msg['date'])
        print(msg['Authentication-Results'])
        # print("Message content[{}]:{}".format(n, content))

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(
                        decode=True)  # to control automatic email-style MIME decoding (e.g., Base64, uuencode, quoted-printable)
                    body = body.decode()

                elif part.get_content_type() == "text/html":
                    continue



IMAP_fetch_emails(server, user, password)