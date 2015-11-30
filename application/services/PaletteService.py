import PIL
from PIL import Image, ImageDraw
import io
from ..models.ImageModel import ImageModel


class PaletteService():

    @staticmethod
    def getPalette(image_id):

        image = ImageModel.get_by_id(int(image_id))
        
        colors = PaletteService.get_colors(image.image)


        baseColor = colors[0][1]
        distances = []

        for color in colors[:20]:
            distances.append(PaletteService.color_distance(baseColor, color[1]))

        complIndex = distances.index(max(distances))

        return {
            'primary' : PaletteService.rgb_to_hex(colors[0][1]), 
            'secondary' : PaletteService.rgb_to_hex(colors[1][1]),
            'accent' : PaletteService.rgb_to_hex(colors[complIndex][1]),
        }


    @staticmethod
    def get_colors(inImage, numcolors=20, resize=150):

        image = Image.open(io.BytesIO(inImage))
        image = image.resize((resize, resize))
        result = image.convert('RGB', palette=Image.ADAPTIVE, colors=numcolors)
        result.putalpha(0)
        colors = result.getcolors(resize*resize)

        colors.sort(cmp=lambda x,y: cmp(y[0], x[0]))

        return colors

    @staticmethod
    def color_distance(rgb1,rgb2):
        rm = 0.5*(rgb1[0]+rgb2[0])
        diff = ((rgb1[0]-rgb2[0])**2+(rgb1[1]-rgb2[1])**2+(rgb1[2]-rgb2[2])**2)**0.5
        d = sum((2+rm,4,3-rm)*int(diff)**2)**0.5
        return d

    @staticmethod
    def rgb_to_hex(color):
        return '#' + (''.join(chr(c) for c in color[0:3]).encode('hex'))
