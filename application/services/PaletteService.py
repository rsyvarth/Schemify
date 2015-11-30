import PIL
from PIL import Image, ImageDraw
import io
from ..models.ImageModel import ImageModel


class PaletteService():

    @staticmethod
    def getPalette(image_id):

        image = ImageModel.get_by_id(int(image_id))
        
        colors = PaletteService.get_colors(image.image)

        return {
            'primary' : PaletteService.rgb_to_hex(colors[0][1]), 
            'secondary' : PaletteService.rgb_to_hex(colors[1][1]),
            'accent' : PaletteService.rgb_to_hex(colors[2][1]),
        }


    @staticmethod
    def get_colors(inImage, numcolors=10, resize=150):

        image = Image.open(io.BytesIO(inImage))
        image = image.resize((resize, resize))
        result = image.convert('RGB', palette=Image.ADAPTIVE, colors=numcolors)
        result.putalpha(0)
        colors = result.getcolors(resize*resize)

        colors.sort(cmp=lambda x,y: cmp(y[0], x[0]))

        return colors

    @staticmethod
    def rgb_to_hex(color):
        return '#' + (''.join(chr(c) for c in color[0:3]).encode('hex'))
