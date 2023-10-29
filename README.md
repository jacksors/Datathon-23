![doodleduel logo](https://i.imgur.com/ly8RKOv.png)
# DoodleDuel!
## What it does
Draw pictures on a canvas and have the AI guess what you are drawing after each stroke with high accuracy.
## How we built it
The model is a custom PyTorch model similar to ResNet 18 but adapted for our specific use case and trained on the sample data provided. The model converts the strokes into a 256x256 image before running classifications. The web portion was built on a Next.js frontend and django backend to allow easy interaction with our model.
## Challenges we ran into
Overfitting was a recurring problem during training. This was mitigated by lowering learning rate, increasing dropout rate, and adjusting batch size continuously until we could no longer decrease loss by any of these methods.
## Accomplishments that we're proud of
The model completed training with a 0.9 validation accuracy. Furthermore the classes had relatively consistent F1 scores with the lowest at 0.84.
## What we learned
We learned about all of the nuances it takes to build and train a successful image classification model. 
## What's next for DoodleDuel
We would like to experiment with making the model larger to increase data. We also would like to incorporate the user feedback that we collect to continuously train the model on new classes.
## Classification Report
![classification report](https://i.imgur.com/NcdDmZw.png)
