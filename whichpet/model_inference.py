from fastai.vision import load_learner, open_image, Learner
from whichpet.images import rotate_image_by_exif, crop_image, resize_image
import os

# Class to hold the result of the inference
class Result:
  def __init__(self, path, filename, category, display_category, percentage, info):
    self.path = path
    self.filename = filename
    self.category = category
    self.display_category = display_category
    self.percentage = percentage
    self.info = info


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
  pred_class, __, outputs = learn.predict(image)

  # Convert the pred_class to a string category
  category = str(pred_class)

  # Get the percentage confidence (as an integer eg 97%)
  category_index = learn.data.classes.index(category)
  confidence = round(outputs[category_index].item()  * 100)

  # Get the friendly category name to display
  display_category = friendly_class_name(category)

  # Get just the filename from the path
  head, filename  = os.path.split(image_path)

  # copy to a result object
  r = Result(image_path, filename, category, display_category, confidence, info)

  return r


# Calling point to run the prediction on a given image
# We do some image manipulation here
def do_inference(learn, image_path):

  # initialise the results
  results = []

  # Run on original image
  r1 = run_model(learn, image_path, "Original image")
  results.append(r1)

  # Photos can be in the incorrect orientation
  rotated_path = rotate_image_by_exif(image_path, "rotated")
  if rotated_path != "":
    r2 = run_model(learn, rotated_path, "Rotated to correct orientation")
    results.append(r2)

  # Try cropping the image by 10% to see if we get a better result
  cropped_path = crop_image(image_path, 0.10, "_cropped_10")
  r3 = run_model(learn, cropped_path, "Cropped by 10%")
  results.append(r3)

  return results


#def saveResults(user_feedback): TODO