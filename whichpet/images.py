import os
from PIL import Image, ExifTags

# Save PIL image to file
def save_image(image, orig_path, suffix):
  file, __ = os.path.splitext(orig_path)
  new_path = orig_path.replace(file, file + "_" + suffix)

  # convert RGBA to RGB
  if (image.mode == 'RGBA'):
      image = image.convert('RGB')

  image.save(new_path, "JPEG")
  image.close()

  return new_path

# open image, check if it needs rotating based on exif data
# if it does save as new file with _label as suffix and return path
# otherwise return empty string
def rotate_image_by_exif(image_path, label):
    img = Image.open(image_path)
    rotate_by = get_exif_rotation(img)

    if (rotate_by == 0):
        img.close()
        return ""

    rotated_image = img.rotate(rotate_by, expand=True)
    return save_image(rotated_image, image_path, label)

# Retrieve exif data and determine the degrees of rotation required
# See https://en.wikipedia.org/wiki/Exif
def get_exif_rotation(image):
    rotate_by = 0
    try:
        for orientation in ExifTags.TAGS.keys():
            if (ExifTags.TAGS[orientation] == 'Orientation'):
                break

        exif = dict(image._getexif().items())
        if exif[orientation] == 3:
            rotate_by = 180
        elif exif[orientation] == 6:
            rotate_by = 270
        elif exif[orientation] == 8:
            rotate_by = 90

        return rotate_by
    except (AttributeError, KeyError, IndexError):
        # image has no exif data
        return 0

# Crop image by specified amount on each edge
# for example 0.10 reduces each edge by 10%
def crop_image(image_path, shrink_by, label):
    img = Image.open(image_path)
    w = img.width
    h = img.height

    crop_width = round(w * shrink_by)
    crop_height = round(h * shrink_by)

    w1 = crop_width
    w2 = w - crop_width
    h1 = crop_height
    h2 = h - crop_height
  
    crop_rectangle = (w1, h1, w2, h2)
    cropped_img = img.crop(crop_rectangle) 
    return save_image(cropped_img, image_path, label)

# Resizes image keeping aspect ratio. The longest edge is now the specified size.
# eg 2000 x 3000 with max_size 300 becomes 200 x 300
def resize_image(image_path, max_size, label):
    img = Image.open(image_path)
    size = max_size,max_size
    img.thumbnail(size, Image.NEAREST)
    return save_image(img, image_path, label)