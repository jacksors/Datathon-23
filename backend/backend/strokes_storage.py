# strokes_storage.py

strokes_data = []

def get_strokes():
    return strokes_data.copy()

def add_stroke(stroke):
    strokes_data.append(stroke)
    print(strokes_data)

def clear_strokes():
    strokes_data.clear()
    print(strokes_data)
