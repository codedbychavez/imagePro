from pathlib import Path
from pathlib import Path
from PIL import Image, ImageOps
import smartcrop
import json

from helper_functions import BackgroundColorDetector, get_file_name, download_image, get_blur_score

BASE_DIR = Path(__file__).resolve().parent

def my_function():
    return "Result from my function"

def crop_image_to_bounding_box(file_path_to_image, image_file_name):
    result = {}

    try:
        file_name = image_file_name
        # Open and load the image
        image = Image.open(file_path_to_image)
        image.load()
        image_size = image.size
        # Remove alpha channel
        invert_image = image.convert("RGB")
        # Invert the image so that white is 0
        invert_image = ImageOps.invert(invert_image)
        image_box = invert_image.getbbox()
        # Crop the image based on the image box
        cropped = image.crop(image_box)
        # Save the image to the media path
        file_path = Path.joinpath(
            BASE_DIR, 'input_images/{0}'.format(file_name))
        cropped.save(str(file_path))

        new_size = cropped.size
        result = {
            'size': image_size,
            'new_size': new_size,
            'cropped_image_file_path': str(file_path),
            'success': True
        }

    except:
        result = {
            'success': False,
            'error': 'Unable to crop the image to the object'
        }

    return result


# def apply_smart_cropping_to_image(image_url):
#     downloaded_image = download_image(image_url)
#     file_name = get_file_name(image_url)
#     # Open and load the image
#     image = Image.open(str(downloaded_image['file_path']))
#     # Initialize smart crop
#     sc = smartcrop.SmartCrop()
#     # smart crop the image
#     result = sc.crop(image, 700, 700)
#     # print the result
#     print(json.dumps(result['top_crop'], indent=2))
#     # get the box that we need to crop
#     box = (
#         result['top_crop']['x'],
#         result['top_crop']['y'],
#         result['top_crop']['width'] + result['top_crop']['x'],
#         result['top_crop']['height'] + result['top_crop']['y']
#     )
#     # crop the image using the box
#     cropped_image = image.crop(box)

#     # Save the image to the media path
#     file_path = Path.joinpath(BASE_DIR, 'media/{0}'.format(file_name))
#     cropped_image.save(str(file_path))
#     result_dict = {
#         'smart_cropped_image_url': '{0}/media/{1}'.format(base_path, file_name)
#     }

#     return result_dict


# def resize_and_square_image(image_url, length):
#     """
#     Resizing strategy : 
#     1) We resize the smallest side to the desired dimension (e.g. 1080)
#     2) We crop the other side so as to make it fit with the same length as the smallest side (e.g. 1080)
#     """
#     downloaded_image = download_image(image_url)
#     file_name = get_file_name(image_url)
#     # Open and load the image
#     image = Image.open(str(downloaded_image['file_path']))

#     result_dict = {}

#     if image.size[0] == image.size[1]:
#         result_dict = {
#             "square_image_result": 'Image is already squared',
#             "success": False,
#         }
#         return result_dict

#     if image.size[0] < image.size[1]:
#         # The image is in portrait mode. Height is bigger than the width

#         # this makes the width fit the LENGTH in pixels while conserving the ration
#         resized_image = image.resize(
#             (length, int(image.size[1] * (length / image.size[0]))))

#         # Amount of pixel to lose in total on the height of the image.
#         required_loss = (resized_image.size[1] - length)

#         # Crop the height of the image so as to keep the center part.
#         resized_image = resized_image.crop(
#             box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))

#         # We now have a length*length pixels image.

#         # Save the image to the media path.
#         file_path = Path.joinpath(BASE_DIR, 'media/{0}'.format(file_name))
#         resized_image.save(str(file_path), 'JPEG', quality=100)
#         result_dict = {
#             'square_image_url': '{0}/media/{1}'.format(base_path, file_name),
#             'success': True,
#         }
#     else:
#         # This image is in landscape mode or already squared. The width is bigger than the height.

#         # This makes the height fit the LENGTH in pixels while conserving the ration.
#         resized_image = image.resize(
#             (int(image.size[0] * (length / image.size[1])), length))

#         # Amount of pixel to lose in total on the width of the image.
#         required_loss = resized_image.size[0] - length

#         # Crop the width of the image so as to keep 1080 pixels of the center part.
#         resized_image = resized_image.crop(
#             box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))

#         # We now have a length*length pixels image.

#         # Save the image to the media path
#         file_path = Path.joinpath(BASE_DIR, 'media/{0}'.format(file_name))
#         resized_image.save(str(file_path), 'JPEG', quality=100)
#         result_dict = {
#             'square_image_url': '{0}/media/{1}'.format(base_path, file_name),
#             'success': True,
#         }

#     return result_dict


def calculate_blur_score(file_path_to_image, blur_threshold):
    image_blur_score = get_blur_score(file_path_to_image, blur_threshold)
    return image_blur_score


# def smartly_equally_apply_padding_to_image(image_url, padding_percentage):
#     """
#     Auto computes the padding color to pad the image with
#     """
#     result_dict = {}
#     try:
#         downloaded_image = download_image(image_url)
#         file_name = get_file_name(image_url)

#         downloaded_image_file_path = str(downloaded_image['file_path'])

#         # Instantiate the background color class
#         BackgroundColor = BackgroundColorDetector(downloaded_image_file_path)

#         # Detect the background color
#         background_color = BackgroundColor.detect()

#         # Open and load the image
#         image = Image.open(downloaded_image_file_path)

#         # Calculate border pixels from padding percentage
#         border_pixels = round((padding_percentage * (image.size[1] / 100)))

#         desired_size = (image.size[0] + border_pixels,
#                         image.size[1] + border_pixels)
#         # desired_size = (desired_width, desired_height) // original - before padding percentage

#         delta_width = desired_size[0] - image.size[0]
#         delta_height = desired_size[1] - image.size[1]
#         pad_width = delta_width // 2
#         pad_height = delta_height // 2
#         padding = (pad_width, pad_height, delta_width -
#                    pad_width, delta_height - pad_height)

#         # Expand the image
#         expanded_image = ImageOps.expand(image, padding, background_color)
#         # print(background_color)

#         # Save the image to the media path.
#         file_path = Path.joinpath(BASE_DIR, 'media/{0}'.format(file_name))
#         expanded_image.save(str(file_path), 'JPEG', quality=100)

#         result_dict = {
#             'pad_image_url': '{0}/media/{1}'.format(base_path, file_name),
#             'success': True
#         }
#     except:
#         result_dict = {
#             'success': False
#         }
#     return result_dict


def equally_apply_padding_to_image(file_path_to_image, padding_percentage, color, file_name):
    """
    A color to pad the image with has be given
    """
    result_dict = {}
    try:

        file_name = file_name

        # Open and load the image
        image = Image.open(file_path_to_image)

        # Calculate border pixels from padding percentage
        border_pixels = round((padding_percentage * (image.size[1] / 100)))

        desired_size = (image.size[0] + border_pixels,
                        image.size[1] + border_pixels)
        # desired_size = (desired_width, desired_height) // original - before padding percentage

        delta_width = desired_size[0] - image.size[0]
        delta_height = desired_size[1] - image.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height, delta_width -
                   pad_width, delta_height - pad_height)

        # Expand the image
        expanded_image = ImageOps.expand(image, padding, color)
        # print(background_color)

        # Save the image to the media path.
        file_path = Path.joinpath(
            BASE_DIR, 'input_images/{0}'.format(file_name))
        expanded_image.save(str(file_path), 'JPEG', quality=100)

        result_dict = {
            'pad_image_url': str(file_path),
            'success': True
        }
    except:
        result_dict = {
            'success': False
        }
    return result_dict


def apply_padding_to_specific_side_of_image(file_path_to_image, pixel_amount_of_padding, color, where, file_name):
    """
    A color to pad the image with has be given
    """
    result_dict = {}
    try:
        file_name = file_name

        # Open and load the image
        image = Image.open(file_path_to_image)

        if where == 'top_bottom':
            # Add padding to the top and bottom using the expand method
            expanded_image = ImageOps.expand(
                image, (0, pixel_amount_of_padding), color)
        elif where == 'left_right':
            # Add padding to the top and bottom using the expand method
            expanded_image = ImageOps.expand(
                image, (pixel_amount_of_padding, 0), color)

        # Save the image to the media path.
        file_path = Path.joinpath(
            BASE_DIR, 'input_images/{0}'.format(file_name))
        expanded_image.save(str(file_path), 'JPEG', quality=100)

        result_dict = {
            'pad_image_url': str(file_path),
            'success': True
        }
    except:
        result_dict = {
            'success': False
        }
    return result_dict
