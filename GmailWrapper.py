import imaplib
import email
import urllib
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from email.header import decode_header
import re
import requests
from datetime import datetime
from CibusVoucher import CibusVoucher
import mailparser

MAIN_OUTPUT_FOLDER = r"C:\Projects\CibusVouchers\Output"

class GmailWrapper:

    def __init__(self, username, password):
        self.userName = username
        self.password = password

    def connect(self):
        # create an IMAP4 class with SSL
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.userName, self.password)

    def getOnlyUnseenEmails(self):
        query = '(UNSEEN X-GM-LABELS "Inbox" FROM "noreply@mysodexo.co.il")'
        return self.getEmails(query, datetime.min.date())

    def getEmailsFromDate(self, fromDate):
        dateQuery = fromDate.strftime("%d-%b-%Y")
        query = '(X-GM-LABELS "Inbox" FROM "noreply@mysodexo.co.il" SINCE "{}")'.format(dateQuery)
        return self.getEmails(query, fromDate)

    def getEmails(self, query, fromDate):
        cibusVoucherList = []
        status, messages = self.mail.select("INBOX")
        type, data = self.mail.search(None, query)
        mail_ids = data[0]
        id_list = mail_ids.split()
        ids_len = len(id_list)
        for i in range(ids_len):
            email_id = id_list[i]
            print("{}  -  {}/{}".format(email_id , i, ids_len))
            try:
                typ, data = self.mail.fetch(email_id, '(RFC822)')

                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_msg = mailparser.parse_from_string(raw_email_string)
                email_date = email_msg.date.date()

                if(email_date >=  fromDate):

                    barname = re.findall('https?:\/\/(?:www\.)?mysodexo\.co\.il\/b\?([-a-zA-Z0-9()@:%_\+.~#?&=]*)', email_msg.body)[0]

                    # Get voucher value
                    subject = email_msg.headers['Subject']
                    decoded_subject, charset = decode_header(subject)[0]
                    voucher_value = re.findall('[\s\S]*?([0-9]+) ', decoded_subject)[0]

                    # Go to bar url and extract barcode
                    link = "https://www.mysodexo.co.il/b?" + barname
                    f = requests.get(link)
                    barcode = re.findall('alt="([0-9]+)"', f.text)[0]

                    # Build image url
                    imgurl = 'https://www.mysodexo.co.il/b/bar.ashx?' + barname
                    title = barcode + '(' + str(voucher_value) + ')'
                    cell = '<div style="text-align:center;flex:1;font-family:Arial;margin-top:2px;margin-bottom:2px;-webkit-transform: rotate(90deg);transform: rotate(90deg);"><img height=1300 width=6000 src="' + imgurl + '" style="padding-top:8px;padding-bottom:8px;display:block;image-rendering:pixelated;" />' + barcode + '(' + str(
                        voucher_value) + ')' + '</div>'
                    response = requests.get(imgurl).raw

                    png_format = "{}\{}.png".format(MAIN_OUTPUT_FOLDER,barcode)
                    jpeg_format = "{}\{}.jpeg".format(MAIN_OUTPUT_FOLDER,barcode)
                    (filename, headers) = urllib.request.urlretrieve(imgurl, png_format)
                    img = Image.open(png_format).convert('RGB').resize((900, 450)).save(jpeg_format, "JPEG", optimize=True)
                    cibusVoucherList.append(CibusVoucher(email_date, voucher_value, barcode, jpeg_format))
                    print("Voucher for {}, value {} barcode {}".format(email_date, voucher_value, barcode))
                else:
                    break
            except Exception as e:
                print(e)
                continue

        return cibusVoucherList









