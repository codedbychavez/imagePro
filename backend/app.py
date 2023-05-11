from flask import Flask, request
from flask_cors import CORS
import math

from functions import calculate_blur_score, crop_image_to_bounding_box, equally_apply_padding_to_image, get_file_name, apply_padding_to_specific_side_of_image

from helper_functions import check_background_color_consistency, clean_up_dir, download_image, calculate_image_dimensions, base64_encode_image

app = Flask(__name__)
CORS(app)

@app.post("/api/process-images")
def process_images():
    """
    The main image processing endpoint
    """
    results = []
    # Extract data from request
    post_data = request.get_json()
    data = {
        'resolution_width_min': post_data['resolution_width_min'],
        'resolution_height_min': post_data['resolution_height_min'],
        'square_images': post_data['square_images'],
        'blur_check': post_data['blur_check'],
        'blur_threshold': post_data['blur_threshold'],
        'padding_remove': post_data['padding_remove'],
        'padding_add': post_data['padding_add'],
        'images': post_data['images']
    }

    # Loop through the list of images
    for image_url in data['images']:
        image_success_state = True
        error_messages = []
        error_codes = []
        image_result_dictionary = {}

        downloaded_image = download_image(image_url)
        image_dimensions = calculate_image_dimensions(downloaded_image)
        is_image_already_squared = False

        # Check if the image is already squared
        if image_dimensions['width'] == image_dimensions['height']:
            is_image_already_squared = True

        image_result_dictionary['src_original'] = image_url
        image_file_name = get_file_name(image_url)
        image_result_dictionary['file_name'] = image_file_name

        # Check image dimensions
        if image_dimensions['width'] < data['resolution_width_min']:
            size_error = 'image is only {0}px wide and your minimum is set to {1}px'.format(
                image_dimensions['width'], data['resolution_width_min'])
            error_messages.append(size_error)
            error_codes.append("SIZE")
            image_success_state = False

        # Calculate the image blur score
        blur_check_result = calculate_blur_score(
            downloaded_image, data['blur_threshold'])
        if blur_check_result['blurry_score'] < data['blur_threshold']:
            blur_error = 'image blur score is {0} which is quite blurry and breaches your threshold of {1}'.format(
                blur_check_result['blurry_score'], data['blur_threshold'])
            error_messages.append(blur_error)
            error_codes.append("BLURRY")
            image_success_state = False

        image_result_dictionary['blurry'] = blur_check_result['blurry']
        image_result_dictionary['blurry_score'] = blur_check_result['blurry_score']


        # Note before cropping we have to check if the background color is even - consistent across the top (left to right) and left edge (top to bottom)

        image_background_consistency_check_result = check_background_color_consistency(
            downloaded_image, 12)
        # {'average_background_color': {'consistent': True, 'color': (238, 239, 244)}, 'score': 0.0, 'similar': True} -> When similar
        # {'similar': False} -> When not similar

        if (image_background_consistency_check_result['similar'] == False):
            print('Similarity is false. Skipping crop operation...')

        elif (image_background_consistency_check_result['similar'] == True):
            # Do crop operation if needed
            # {'average_background_color': {'consistent': False, 'color': (236, 236, 244)}, 'score': 9.582524649533328, 'similar': True}

            # IMAGE MANIPULATIONS
            # Create a variable to hold the url of the manipulated image as we go along
            manipulated_image_file_path = downloaded_image

            # 1. CROP OPERATION!

            crop_image_result = None
            if data['padding_remove'] == True:
                crop_image_result = crop_image_to_bounding_box(manipulated_image_file_path, image_file_name)

                if crop_image_result['success'] == True:
                    manipulated_image_file_path = crop_image_result['cropped_image_file_path']
                    # Check if image is still squared after crop
                    image_dimensions_after_crop = calculate_image_dimensions(manipulated_image_file_path)
                    # Check if the image is already squared
                    if image_dimensions_after_crop['width'] == image_dimensions_after_crop['height']:
                        is_image_already_squared = True
                    else: is_image_already_squared = False
                else:
                    error_messages.append(crop_image_result['error'])
                    error_codes.append('CROP')
                    image_success_state = False

            # 2. PAD OPERATION!

            # To pad image --> result from the image_background_consistency_check -->
            # If similarity if true, use average_background_color --> It will always be true in this case since the wrapper if checks that it is already true

            if data['padding_add'] != 0:
                # 1. Get the average background color to create the padding from
                average_background_color = image_background_consistency_check_result[
                    'average_background_color']['color']

                if is_image_already_squared == True:
                    # Equally apply padding to all the edges
                    image_url_to_pad = manipulated_image_file_path
                    file_url_of_padded_image = None
                    pad_image_result = equally_apply_padding_to_image(
                        image_url_to_pad, data['padding_add'], average_background_color, image_file_name)

                    if pad_image_result['success'] == True:
                        file_url_of_padded_image = pad_image_result['pad_image_url']
                        manipulated_image_file_path = file_url_of_padded_image

                # SQUARE OPERATION!

                elif is_image_already_squared == False:
                    # Apply padding to specific edges of the image (top_bottom, left_right)
                    image_url_to_square = manipulated_image_file_path
                    # 1. Determine the shorter side of the image (width, height)
                    shorter_image_side = 0
                    longer_image_side = 0
                    if image_dimensions['width'] > image_dimensions['height']:
                        shorter_image_side = image_dimensions['height']
                        longer_image_side = image_dimensions['width']
                    else:
                        shorter_image_side = image_dimensions['width']
                        longer_image_side = image_dimensions['height']

                    # Compute the distance between the shorter and longer side
                    # We're dividing the distance by 2 to have the padding equally apply to the edges of the image
                    difference_between_longer_and_shorter_side = math.floor(
                        (longer_image_side - shorter_image_side) / 2)

                    if shorter_image_side == image_dimensions['width']:
                        print('Add padding to the left and right edges')
                        square_image_result = apply_padding_to_specific_side_of_image(
                            image_url_to_square, difference_between_longer_and_shorter_side, average_background_color, 'left_right', image_file_name)
                        if square_image_result['success'] == True:
                            file_url_of_squared_image = square_image_result['pad_image_url']
                            manipulated_image_file_path = file_url_of_squared_image

                    elif shorter_image_side == image_dimensions['height']:
                        print('Add padding to the top and bottom edge of the image')
                        square_image_result = apply_padding_to_specific_side_of_image(
                            image_url_to_square, difference_between_longer_and_shorter_side, average_background_color, 'top_bottom', image_file_name)
                        if square_image_result['success'] == True:
                            file_url_of_squared_image = square_image_result['pad_image_url']
                            manipulated_image_file_path = file_url_of_squared_image

        # 4. ENCODING

        # Encode the image as a base64 string

        base64_encoded_image = base64_encode_image(manipulated_image_file_path)

        if base64_encoded_image['success'] == True:
            image_result_dictionary['base64'] = base64_encoded_image['base64']

        image_result_dictionary['error_message'] = error_messages
        image_result_dictionary['error_code'] = error_codes

        # Success was set to False based on the following conditions:
        # 1. Image does has not met the minimum requirements
        # 2. The image blur score is less than or equal to 100
        # 3. Cropping has failed
        image_result_dictionary['success'] = image_success_state

        results.append(image_result_dictionary)

    # Remove all the images from the input_images folder
    clean_up_dir()

    return {
        "results": results
    }

if __name__ == "__main__":
    app.run(debug=True)