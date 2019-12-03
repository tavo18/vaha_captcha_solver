from PIL import Image
from io import BytesIO

im = Image.open("/home/tavo/Escritorio/carInfoScrapper/dataset/examples/2.png")
ancho, alto = im.size
letra1 = im.crop((9, 0, 23, alto))
letra2 = im.crop((23, 0, 37, alto))
letra3 = im.crop((35, 0, 49, alto))
letra4 = im.crop((49, 0, 63, alto))
letra5 = im.crop((61, 0, 75, alto))
letra6 = im.crop((75, 0, 89, alto))

letra1.show()
letra2.show()
letra3.show()
letra4.show()
letra5.show()
letra6.show()
# sub_image = full_image[y_start: y_end, x_start:x_end]