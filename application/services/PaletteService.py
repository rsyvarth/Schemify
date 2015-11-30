import PIL
from PIL import Image, ImageDraw
import io
from ..models.ImageModel import ImageModel


class PaletteService():

    @staticmethod
    def getPalette(image_id):

        amount_to_consider = 40 
        image = ImageModel.get_by_id(int(image_id))
        colors = [item[1] for item in PaletteService.get_colors(image.image)[:amount_to_consider]]

        baseColor = colors[0]

        def distance_from_base(color):
            return PaletteService.color_distance(baseColor, color)

        #sort top colors by distance
        colors.sort(cmp=lambda x,y: distance_from_base(x) < distance_from_base(y));

        complIndex1 = len(colors)/2
        complIndex2 = len(colors) -1

        return {
            'primary' : PaletteService.rgb_to_hex(colors[0]), 

            'secondary' : PaletteService.rgb_to_hex(colors[complIndex1]),

            'accent' : PaletteService.rgb_to_hex(colors[complIndex2]),
        }


    @staticmethod
    def get_colors(inImage, numcolors=20, resize=150):

        image = Image.open(io.BytesIO(inImage))
        image = image.resize((resize, resize))
        result = image.convert('P', colors=numcolors)
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
