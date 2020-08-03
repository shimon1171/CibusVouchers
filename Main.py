from datetime import datetime, timedelta
import sys
import json
from TelegramWrapper import TelegramWrapper
from GmailWrapper import GmailWrapper


def Main(jsonFilePath):

    # read all configuration from 'config.json' file.
    # The file content is :
    # {
    #     "GmailUserMame": "<User name>@gmail.com",
    #     "GmailPassword": "<Password>",
    #     "TelegramToken": "<Token>",
    #     "TelegramChatId": "<Chat Id>"
    # }
    try:
        with open(jsonFilePath) as json_file:
            data = json.load(json_file)
            # gmail credentials
            password = str(data["GmailPassword"])
            username = str(data["GmailUserMame"])
            # telegram credentials
            telegram_chat_id = str(data["TelegramChatId"])
            telegram_token = str(data["TelegramToken"])

        print("Read config")
        # Get voucher form gmail
        gmailWrapper = GmailWrapper(username, password)
        gmailWrapper.connect()

        # Example of how we can get all the unseen email
        cibusVoucherList = gmailWrapper.getOnlyUnseenEmails()

        # example how we can get all email for certain date.
        yesterday = (datetime.now() - timedelta(1)).date()
        #cibusVoucherList = gmailWrapper.getEmailsFromDate(yesterday)

        # Send voucher to Telegram
        telegramWrapper = TelegramWrapper(telegram_chat_id, telegram_token)
        for cibusVoucher in cibusVoucherList:
            cibusVoucher.SendCibusVoucherToTelegram(telegramWrapper)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    print("Start")
    if(len(sys.argv) != 2):
        print("The script input is json file path, we will set the jsom file to local folder")
        jsonFilePath = 'config.json'
    else:
        jsonFilePath = sys.argv[1]
    print(jsonFilePath)
    Main(jsonFilePath)
