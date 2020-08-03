from PIL import Image, ImageDraw, ImageFont

class ImageHelper:

    def __init__(self, orignal_path):
        self.orignal_path = orignal_path
        self.font_size = 35
        self.font = ImageFont.truetype("arial.ttf", self.font_size)

    def SaveTextLinesToImage(self,listOfLines, outputFile):
        img = Image.open(self.orignal_path)
        img_src_w, img_src_h = img.size
        background = Image.new('RGB', (img_src_w + 5, img_src_h + 200), 'white')
        bg_w, bg_h = background.size
        offset = ((bg_w - img_src_w) // 2, 50)
        background.paste(img, offset)
        background.save(outputFile)

        img = Image.open(outputFile, 'r')
        draw = ImageDraw.Draw(img)
        h = img_src_h + 50 + 2
        for textLine in listOfLines:
            self.AddText(textLine, draw, bg_w, h)
            h = h + self.font_size
        img.save(outputFile)


    def AddText(self, text, draw, middel_of_img , h):
        text_w, text_h = draw.textsize(text, self.font)
        draw.text(((middel_of_img - text_w) // 2, h), text, 'black', font=self.font)
