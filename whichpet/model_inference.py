from fastai.vision import load_learner, open_image, Learner
from whichpet.images import rotate_image_by_exif, crop_image, resize_image
from operator import attrgetter
import os


# Class to hold the result of the inference
class Result:
  def __init__(self, path, filename, info, prediction, other_predictions):
    self.path = path
    self.filename = filename
    self.info = info
    self.prediction = prediction
    self.other_predictions = other_predictions

class Prediction:
  def __init__(self, category, display_category, percentage):
    self.category = category
    self.display_category = display_category
    self.percentage = percentage

# Load the trained model (only do this once) from the pkl file
def init_model(model_path):
  learn = load_learner(model_path)
  return learn

# A function that converts the class name into a friendly label
# eg american_pit_bull_terrier --> American Pit Bull Terrier
def friendly_class_name(class_name):
  return class_name.replace("_", " ").title()

# Run the model passing in the following:
# Learn - learner
# image_path - path to test image
# info - information for this result which can be displayed to the user
def run_model(learn, image_path, info):

  # Get the image
  image = open_image(image_path)

  # Run the prediction
  __, __, outputs = learn.predict(image)

  # Convert the results to a list of predictions
  predictions = convert_to_predictions(outputs, learn.data.classes)
  prediction = predictions[0]

  if len(predictions) == 1:
    other_predictions = []
  else:
    del predictions[0] 
    other_predictions = predictions

  # Get just the filename from the path
  __, filename  = os.path.split(image_path)

  # copy to a result object
  r = Result(image_path, filename, info, prediction, other_predictions)

  return r

# Convert the results to a list of Predictions
# where the rounded up percentage > 0 
# (ie 0.66 --> 66% but 0.00006 => 0%)
def convert_to_predictions(outputs, classes):
    predictions = []
    for idx, category in enumerate(classes):
      percentage = round(outputs[idx].item()  * 100)
      if percentage > 0:
        display_category = friendly_class_name(category)
        pred = Prediction(category, display_category, percentage)
        predictions.append(pred) 
    predictions.sort(key=lambda x: x.percentage, reverse=True)
    return predictions


# Calling point to run the prediction on a given image
# We do some image manipulation here
def do_inference(learn, image_path):

  # Photos can be in the incorrect orientation
  rotated_path = rotate_image_by_exif(image_path, "rotated")
  is_rotated = rotated_path != ""
  if is_rotated:
    image_path = rotated_path
    info = "Rotated to correct orientation"
  else:
    info = "Original image"

  # Run on original image
  r1 = run_model(learn, image_path, info)

  # Try cropping the image by 10% to see if we get a better result
  path_to_crop = image_path
  cropped_path = crop_image(path_to_crop, 0.10, "_cropped_10")
  r2 = run_model(learn, cropped_path, info +", cropped by 10%")

  # Get the best result
  best_result = r2 if r2.prediction.percentage > r1.prediction.percentage else r1

  # Return result
  return best_result
