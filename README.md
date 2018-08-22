# Image Resizer
***
Script resizes provided image.
- you can choose certain width/height or just scale of output image.
(if you specify both scale and width/height **it will cause error** )
- you can choose output dir or leave it blank.
(script will save output image in source dir and name it as <original_name_widthXheight> )

## Usage
* Install requirement modules:
```bash
$ pip install -r requirements.txt
```
* Run
```bash
$ python image_resizer.py -i <path_to_source_image> -d <output_dir> -w <width> -ht <height> -s <scale>
```

 path_to_image and one of three size attributes is **required**

### Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
