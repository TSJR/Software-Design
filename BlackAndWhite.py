from PIL import Image
import numpy

def get_brightness(rgb):
    rgb = [(val / 255) for val in rgb]
    brightness = 0
    brightness += rgb[0] * 0.21
    brightness += rgb[1] * 0.72
    brightness += rgb[2] * 0.07
    brightness *= 100
    # In percent
    return int(brightness)

def get_black_and_white(img, threshold):

    abs_width = 250
    width, height = img.size
    aspect_ratio = width / height
    img = img.resize((abs_width, int(abs_width / aspect_ratio)))

    new_img = Image.new(mode="RGB", size=(img.size))
    pixels = numpy.asarray(img)

    for row in range(len(pixels)):
        for col in range(len(pixels[0])):
            if get_brightness(pixels[row][col]) < threshold:
                new_img.putpixel((col, row), (0, 0, 0))
            else:
                new_img.putpixel((col, row), (255, 255, 255))

    return new_img
