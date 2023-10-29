from PIL import Image, ImageDraw
import pandas as pd
import numpy as np


def strokes_to_image(strokes: pd.DataFrame, canvas_size=(256, 256)):
    # Normalize the strokes to canvas size
    all_x = np.concatenate([stroke[0] for stroke in strokes])
    all_y = np.concatenate([stroke[1] for stroke in strokes])
    min_x, max_x = np.min(all_x), np.max(all_x)
    min_y, max_y = np.min(all_y), np.max(all_y)
    
    # Calculate the scale factor
    scale = min(
        canvas_size[0] / (max_x - min_x),
        canvas_size[1] / (max_y - min_y)
    )
    
    # Calculate the translation needed to center the strokes
    x_translation = (canvas_size[0] - scale * (max_x - min_x)) / 2
    y_translation = (canvas_size[1] - scale * (max_y - min_y)) / 2
    
    # Normalize the strokes
    for stroke in strokes:
        stroke[0] = (stroke[0] - min_x) * scale + x_translation
        stroke[1] = (stroke[1] - min_y) * scale + y_translation
        
    # Draw the strokes on a canvas
    image = Image.new("L", canvas_size, color=255)  # "L" mode is grayscale
    draw = ImageDraw.Draw(image)

    for stroke in strokes:
        xs = stroke[0]
        ys = stroke[1]
        for i in range(1, len(xs)):
            draw.line((xs[i-1], ys[i-1], xs[i], ys[i]), fill="black", width=3)

    image.save("img.png")
    return image