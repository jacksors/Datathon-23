# strokes_storage.py

import redis

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

def get_strokes():
    # Get strokes data from Redis
    strokes_data = r.lrange('strokes', 0, -1)
    # Convert bytes to list of lists of floats
    strokes = [eval(stroke.decode('utf-8')) for stroke in strokes_data]
    return strokes

def add_stroke(stroke):
    # Add a stroke to the list in Redis
    r.rpush('strokes', str(stroke))


def clear_strokes():
    # Clear the strokes data in Redis
    r.delete('strokes')


# # strokes_storage.py

# strokes_data = []

# def get_strokes():
#     return strokes_data.copy()

# def add_stroke(stroke):
#     strokes_data.append(stroke)
#     print(strokes_data)

# def clear_strokes():
#     strokes_data.clear()
#     print(strokes_data)
