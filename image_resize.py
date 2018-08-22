from PIL import Image
import argparse
import os


def get_original_image(path):
    try:
        return Image.open(path)
    except OSError:
        return None


def is_args_valid(args):
    if args.scale and args.scale < 0:
        return False
    if args.width and args.width < 0:
        return False
    if args.height and args.height < 0:
        return False
	if args.scale and (args.width or args.height):
		return False
	if not args.width and not args.height and not args.scale:
        return False
    return True


def check_same_aspect_ratio(width, height, new_width, new_height):
    orig_ratio = round(width/height, 1)
    new_ratio = round(new_width/new_height, 1)
    if orig_ratio != new_ratio:
        answer = input("""New proportion {} is not like original {}\n
        Do You want to proceed (Y/N):""".format(new_ratio, orig_ratio)).upper()
        if answer != "Y":
            return False
    return True


def get_new_size(orig_width, orig_height, width, height, scale):
    orig_prop = round(orig_width / orig_height, 1)
    if width and not height and not scale:
        height = int(width / orig_prop)
    elif not width and height and not scale:
        width = int(orig_prop * height)
    elif scale:
        width, height = int(orig_width * scale), int(orig_height * scale)
    return width, height


def get_resized_image(image, new_size):
    return image.resize(new_size, resample=0)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, dest="image_path")
    parser.add_argument("-d", default=None, dest="dest_dir")
    parser.add_argument("-w", type=int, dest="width")
    parser.add_argument("-ht", type=int, dest="height")
    parser.add_argument("-s", type=float, dest="scale")
    args = parser.parse_args()
    return args


def save_image(image, image_dir, image_name):
    image_path = os.path.join(image_dir, image_name)
    try:
        image.save(image_path)
        return True
    except FileNotFoundError:
        return False


def get_new_name(dest_dir, orig_name, width, height, orig_ext):
    if not dest_dir:
        return "{}_{}x{}{}".format(orig_name, width, height, orig_ext)
    else:
        return orig_name + orig_ext


def get_output_dir(dest_dir, image_path):
    if dest_dir and os.path.isdir(dest_dir):
        return os.path.abspath(dest_dir)
    else:
        return os.path.dirname(image_path)


def main(image_args=None):
    args = get_arguments() or exit("No size arguments")
    if is_args_valid(args):
        exit("args not valid")
    image_path = os.path.abspath(args.image_path)
    orig_image = get_original_image(image_path) or exit("File not found")
    orig_name = os.path.basename(image_path)
    orig_width, orig_height = orig_image.size
    output_dir = get_output_dir(args.dest_dir, image_path)
    new_size = get_new_size(
        *orig_image.size,
        args.width,
        args.height,
        args.scale,
    ) or exit("Wrong aspect_ratio")
    if not check_same_aspect_ratio(*orig_image.size, *new_size):
        exit("wrong aspect ratio")
    new_image = get_resized_image(orig_image, new_size)
    if not dest_dir:
        orig_name = "{0}_{2}x{3}{1}".format(
		*os.path.splitext(orig_name),
		*new_size, 
	)
    if os.path.exists(os.path.join(output_dir, orig_name)):
        exit("File exist")
    if save_image(new_image, output_dir, orig_name):
        print("Saved")
    else:
        print("Directory not found")


if __name__ == "__main__":
    main()
