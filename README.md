# imagePro

This is a python api for processing and enhancing images.

Let's get started.

This project is composed of two parts. The **frontend** and the **backend**. You can use it entirely (frontend and backend) or use its API. 

## Build and run the backend (The API)

1. Point your terminal to the `backend` folder, create a virtual environment and activate it:

```sh
python3 -m venv venv
```

```sh
. venv/bin/activate
```

2. Install the required packages from the `requirements.txt` file:

```sh
pip3 install -r requrements.txt
```

3. Run the application:

```sh
flask run
```

The app can be accessed at: <http://127.0.0.1:5000>. See [Processing images](https://github.com/coldbrewstudios/image-processor-tool#processing-images) for more details.

## Running the backend with Docker

NOTE: The docker container **does not** include the frontend.

1. Have docker installed on your PC/ Mac.

2. Build the docker image and run the container with:

```sh
docker-compose up
```

3. The API can be accessed at: `http://127.0.0.1:5000/`

## Using the backend (API) to processing images

Endpoint: `http://127.0.0.1:5000/api/process-images`  
Method: `POST`  
Body:

```json
{
    "resolution_width_min": 1000,
    "resolution_height_min": 1000,
    "square_images": true,
    "blur_check": true,
    "blur_threshold": 100,
    "padding_remove": false,
    "padding_add": 50,
    "images": [
      "https://www.salton.co.za/wp-content/uploads/2019/08/2200W-HAIR-DRYER.jpg",
      "https://images.pexels.com/photos/18105/pexels-photo.jpg"
    ]
}
```

Sample response:

```json
{
    "results": [
        {
            "base64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCASwBLADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/...",
            "blurry": false,
            "blurry_score": 111,
            "error_code": [
                "SIZE"
            ],
            "error_message": [
                "image is only 800px wide and your minimum is set to 1000px"
            ],
            "file_name": "2200W-HAIR-DRYER.jpg",
            "src_original": "https://www.salton.co.za/wp-content/uploads/2019/08/2200W-HAIR-DRYER.jpg",
            "success": false
        },
        {
            "base64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAMLAwsDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+/...",
            "blurry": false,
            "blurry_score": 231,
            "error_code": [
                "SIZE"
            ],
            "error_message": [
                "image is only 519px wide and your minimum is set to 1000px"
            ],
            "file_name": "c0fc0a_dd0c3e59b6ea4ef2b15df287884f31ec~mv2.jpg",
            "src_original": "https://static.wixstatic.com/media/c0fc0a_dd0c3e59b6ea4ef2b15df287884f31ec~mv2.jpg/v1/fill/w_519,h_519,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/c0fc0a_dd0c3e59b6ea4ef2b15df287884f31ec~mv2.jpg",
            "success": false
        }
    ]
}
```

## Running the frontend

1. Point your terminal to the `frontend` folder.
2. Run `npm install` to install the frontend dependencies.
3. Start the frontend dev server with the following command:

```sh
npm run dev
 ```
 
 ![Snip20230513_2](https://github.com/codedbychavez/imagepro/assets/74829200/35895d94-c4ee-4fab-85f6-ad91b0581532)
 
 4. Define the modifications you need and input the URLs of the images that you want to process. Click the **Process Images** button and wait a few moments.

The results will look like:

![Snip20230513_1](https://github.com/codedbychavez/imagepro/assets/74829200/8f91b427-932f-486b-9d4a-e965630e4ca9)


## Contributions

Contributions are welcomed!

## Developer

[codedbychavez](https://github.com/codedbychavez)


## Options

**resolution_width_min** - The minimum resolution width you want to check for.  
**resolution_height_min** - The minimum resolution width you want to check for.  
**square_images** - If set to true, the beckend processor will square the image.  
**blur_check** - If set to true, the backend processor will tell you if the image is blurry based on the blur threshold you specify.  
**blur_threshold** - The minimum amount of blurriness you want the backend processor to check for.  
**padding_remove** - If set to true, removes the padding from the image.  
**padding_add** - The amount of padding you want to add to the image.  
