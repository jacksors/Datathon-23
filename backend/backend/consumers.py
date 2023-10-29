import json
from channels.generic.websocket import AsyncWebsocketConsumer
from model.predict import predict

class StrokeConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawing = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'clear' in data and data['clear'] is True:
            await self.clear_canvas()
        else:
            xs = data['xs']
            ys = data['ys']
            self.drawing.append([xs, ys])
            await self.process_stroke()

    async def clear_canvas(self):
        print('clearing canvas')
        self.drawing = []
        pass

    async def process_stroke(self):
        prediction, prob = predict(self.drawing, "../model/tut2-model.pt", "../model/classes.csv")
        print(prediction, prob)
        await self.send(text_data=json.dumps({
          'prediction': prediction,
          'probability': prob,
        }))
        pass