# Deep Learning Inference App
## Using python, Flask and the fastai library

Based on v3 of the Fastai Deep Learning course (2019)
Fastai: https://www.fast.ai/

Using Oxford IIIT dataset of dog and cat breeds
http://www.robots.ox.ac.uk/~vgg/data/pets/

Basic purpose of web app:
* Classification model trained to identify dog/cat breeds
* Upload an image(or take a photo on a mobile device)
* Manipulate image if needed (ie rotate based on EXIF data)
* Run it against the model
* See the results including the probability %

TODO:
* Allow user feedback