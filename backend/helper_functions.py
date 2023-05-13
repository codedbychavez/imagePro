# Imports
import cv2
import os
import glob
import ssl
import base64
import math

from urllib import request
from PIL import Image
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# Global variables
BASE_DIR = Path(__file__).resolve().parent

# BACKGROUND COLOR CONSISTENCY CHECKER
def check_background_color_consistency(file_path_to_image, similarity_threshold):
  """
  Checks the color similarities between pixels given a similarity_threshold
  """

  # Define initial variables
  result_dict = {}
  y = 0
  x = 0


  # Read the image
  image = cv2.imread(file_path_to_image)

  # Get the dimensions of the image
  pil_image = Image.open(file_path_to_image)

  image_width, image_height = pil_image.size

  # Crop 10px from the left edge of the image
  pixels_to_crop_from_left = 10

  crop_of_left_strip = image[x: image_width, y: pixels_to_crop_from_left]

  # Define where to save the image
  file_path_to_left_strip = Path.joinpath(BASE_DIR, 'input_images/{0}'.format('left_strip.jpg'))

  cv2.imwrite(str(file_path_to_left_strip), crop_of_left_strip)

  # Crop 10px from the top edge of the image
  pixels_to_crop_from_top = 10

  crop_of_top_strip = image[x: pixels_to_crop_from_top, y: image_width]

  # Define where to save the image
  file_path_to_top_strip = Path.joinpath(BASE_DIR, 'input_images/{0}'.format('top_strip.jpg'))

  cv2.imwrite(str(file_path_to_top_strip), crop_of_top_strip)

  # Merge the two strips

  image_1 = Image.open(file_path_to_left_strip)
  image_2 = Image.open(file_path_to_top_strip)

  image_1 = image_1.rotate(90, Image.NEAREST, expand = 1)

  # Compute the image size 
  image_1_size = image_1.size
  image_2_size = image_2.size

  new_image = Image.new('RGB', (2*image_1_size[0], image_1_size[1]), (250, 250, 20))

  new_image.paste(image_1, (0, 0))
  new_image.paste(image_2, (image_1_size[0], 0))

  # Saving the merged image
  file_path_to_merged_image = Path.joinpath(BASE_DIR, 'input_images/{0}'.format('merged_image.jpg'))

  new_image.save(file_path_to_merged_image, 'JPEG')

  # Get the average color of merged image
  BackgroundColorDetectorOfMergedImage = BackgroundColorDetector(str(file_path_to_merged_image))

  background_color_of_merged_image = BackgroundColorDetectorOfMergedImage.detect()

  # Use the BackgroundColorDetector class to compute the background color of the images

  BackgroundColorDetectorOfTopStrip = BackgroundColorDetector(str(file_path_to_top_strip))

  BackgroundColorDetectorOfLeftStrip = BackgroundColorDetector(str(file_path_to_left_strip))

  # Detect the background color
  background_color_of_top_strip = BackgroundColorDetectorOfTopStrip.detect()
  background_color_of_left_strip = BackgroundColorDetectorOfLeftStrip.detect()

  print(background_color_of_left_strip)
  print(background_color_of_top_strip)

  #  Compute the similarity
  print('Computing similarity...')
  result_dict['average_background_color'] = background_color_of_merged_image

  # Finding pixel color similarity 
  (top_r, top_g, top_b) = background_color_of_top_strip['color']
  (left_r, left_g, left_b) = background_color_of_left_strip['color']

  background_color_of_top_strip = sRGBColor(top_r, top_g, top_b)
  background_color_of_left_strip = sRGBColor(left_r, left_g, left_b)

  background_color_of_top_strip_lab = convert_color(background_color_of_top_strip, LabColor)
  background_color_of_left_strip_lab = convert_color(background_color_of_left_strip, LabColor)

  # Find color difference / similarity
  delta_e = delta_e_cie2000(background_color_of_top_strip_lab, background_color_of_left_strip_lab)

  result_dict['score'] = delta_e

  if (delta_e > similarity_threshold):
      result_dict['similar'] = False
  else:
      result_dict['similar'] = True

  print(result_dict)

  return result_dict

# BACKGROUND COLOR DETECTOR
class BackgroundColorDetector():
  """
  Detects the background color of an image.
  If no specific color stands out then the average color of the 20 most common colors in the image are returned
  """
  def __init__(self, image_path):
    self.img = cv2.imread(image_path, 1)
    self.manual_count = {}
    self.w, self.h, self.channels = self.img.shape
    self.total_pixels = self.w*self.h
    self.result_dict = {}

  def count(self):
    for y in range(0, self.h):
      for x in range(0, self.w):
        RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
        if RGB in self.manual_count:
            self.manual_count[RGB] += 1
        else:
            self.manual_count[RGB] = 1

  def average_color(self):
    red = 0
    green = 0
    blue = 0
    sample = 10
    for top in range(0, sample):
      red += self.number_counter[top][0][0]
      green += self.number_counter[top][0][1]
      blue += self.number_counter[top][0][2]

    average_red = int(red / sample)
    average_green = int(green / sample)
    average_blue = int(blue / sample)
    # print("Average RGB for top ten is: (", average_red,
    #       ", ", average_green, ", ", average_blue, ")")

    return (average_red, average_green, average_blue)

  def twenty_most_common(self):
    self.count()
    self.number_counter = Counter(self.manual_count).most_common(20)
    # for rgb, value in self.number_counter:
        # Prints the 20 most common color
        # print(rgb, value, ((float(value)/self.total_pixels)*100))

  def detect(self):
    self.twenty_most_common()
    self.percentage_of_first = (
        float(self.number_counter[0][1])/self.total_pixels)
    if self.percentage_of_first > 0.5:
        # Background color is consistent
        self.result_dict = {
            'consistent': True,
            'color': self.number_counter[0][0],
        }
        return self.result_dict
    else:
        self.result_dict = {
            'consistent': False,
            'color': self.average_color(),
        }
        return self.result_dict

# GET THE NAME OF A FILE
def get_file_name(file_url):
    """
    Returns the name of a file based on its given path
    """
    parse_url = urlparse(file_url)
    file_path = parse_url.path
    return os.path.basename(file_path)

# ENCODE AN IMAGE AS BASE64
def base64_encode_image(file_path_to_image):
    """
    Encodes an image and returns its base64 string equivalent
    """
    result_dict = {}
    try:
        with open(file_path_to_image, "rb") as img_file:
            base46_string = base64.b64encode(img_file.read())
            base46_string_as_utf8 = base46_string.decode('utf8')
        result_dict = {
            'base64': base46_string_as_utf8,
            'success': True
        }
        return result_dict

    except:
        result_dict = {
            'success': False,
        }
        return result_dict
    
# DOWNLOAD AN IMAGE FROM A GIVEN URL
def download_image(src_original):
    """
    Downloads image from a given url
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    file_name = get_file_name(src_original)
    file_path = Path.joinpath(BASE_DIR, 'input_images/{0}'.format(file_name))
    opener = request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    request.install_opener(opener)
    request.urlretrieve(src_original, file_path)
    # Returns absolute file path of the downloaded image
    return str(file_path)


# CALCULATE IMAGE DIMENSIONS
def calculate_image_dimensions(file_path_to_image):
    """
    Returns the dimension (width, height) for a given image url
    """
    image = Image.open(file_path_to_image)
    width, height = image.size
    return {
        'width': width,
        'height': height
    }

# GET IMAGE BLUR SCORE
def get_blur_score(file_path, threshold):
    """
    Returns the blur score of an image given its file path and an acceptable threshold
    """
    # Initialize variables
    blurry_status = False
    passed = True
    blurry_score = 0

    # Path was converted to its string equivalent for cv2 to use
    image = cv2.imread(str(file_path))

    # Turn the image into grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    blurry_score = fm

    if fm < threshold:
        blurry_status = True
        passed = False

    return {
        "blurry": blurry_status,
        "blurry_score": math.floor(blurry_score),
        "passed": passed
    }

def clean_up_dir():
    files = glob.glob(os.path.join(BASE_DIR, 'input_images/*.jpg'))
    for f in files:
        os.remove(f)