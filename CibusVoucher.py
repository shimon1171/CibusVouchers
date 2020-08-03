import datetime
from ImageHelper import ImageHelper

class CibusVoucher(object):
    def __init__(self, date, voucher_value, barcode, barcode_image_path):
        self.date = date
        self.voucher_value = voucher_value
        self.barcode = barcode
        self.barcode_image_path = barcode_image_path

    def SendCibusVoucherToTelegram(self, telegramWrapper):
        telegramWrapper.send_message(self.getMessage())

        imageHelper = ImageHelper(self.barcode_image_path)
        textLineToadd = []
        textLineToadd.append('91472000011664112345')
        textLineToadd.append('From date {}'.format(datetime.datetime(2020, 7, 29)))
        textLineToadd.append('Value is {}'.format(40))
        imageHelper.SaveTextLinesToImage(textLineToadd, self.barcode_image_path)

        telegramWrapper.send_photo(self.barcode_image_path)

    def getMessage(self):
        return "Voucher for {}, value {} barcode {}".format(self.date, self.voucher_value, self.barcode)