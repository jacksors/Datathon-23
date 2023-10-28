from PIL import Image, ImageDraw
import pandas as pd


def strokes_to_image(strokes: pd.DataFrame, canvas_size=(256, 256)):
    image = Image.new("L", canvas_size, color=255)  # "L" mode is grayscale
    draw = ImageDraw.Draw(image)

    for stroke in strokes:
        xs = stroke[0]
        ys = stroke[1]
        for i in range(1, len(xs)):
            draw.line((xs[i-1], ys[i-1], xs[i], ys[i]), fill="black", width=3)

    image.save("img.png")
    return image