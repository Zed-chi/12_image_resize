from PIL import Image, ImageOps
import argparse
import os


def get_original_image(path):
    try:
        return Image.open(path)
    except OSError:
        return None


def check_same_aspect_ratio(orig_prop, new_prop):
    if orig_prop != new_prop:
        answer = input("""New proportion {} is not like original {}\n
        Do You want to proceed (Y/N): """.format(new_prop, orig_prop)).upper()
        if answer != "Y":
            return None
    return True


def get_new_size(orig_width, orig_height, width, height, scale):
    orig_prop = round(orig_width/orig_height, 1)
    if width and not height and not scale:
        height = int(width / orig_prop)
    elif not width and height and not scale:
        width = int(orig_prop * height)
    elif scale:
        width, height = int(orig_width * scale), int(orig_height * scale)
    new_prop = round(width/height, 1)
    if not check_same_aspect_ratio(orig_prop, new_prop):
        return None
    return width, height


def get_scaled_image(image, new_size):
    return ImageOps.fit(
        image,
        new_size,
        method=0,
        bleed=0.0,
        centering=(0.5, 0.5),
    )


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, dest="image_path")
    parser.add_argument("-d", default=None, dest="dest_dir")
    parser.add_argument("-w", type=int, dest="width")
    parser.add_argument("-ht", type=int, dest="height")
    parser.add_argument("-s", type=float, dest="scale")
    args = parser.parse_args()
    if not args.width and not args.height and not args.scale:
        return None
    return args


def save_image(image, image_dir, image_name):
    image_path = os.path.join(image_dir, image_name)
    if os.path.exists(image_path):
        answer = input(
            "File exists.\n"
            "Do you want to overwrite it?(Y/N):"
            ).upper()
        if answer != "Y":
            return None
    try:
        image.save(image_path)
    except FileNotFoundError:
        print("Directory {} not found, but created.\n".format(image_dir))
        os.mkdir(image_dir)
        image.save(image_path)
    return True


def get_new_name(dest_dir, orig_name, width, height, orig_ext):
    if not dest_dir:
        return "{}_{}x{}{}".format(orig_name, width, height, orig_ext)
    else:
        return orig_name + orig_ext


def get_output_dir(dest_dir, image_path):
    if dest_dir:
        return os.path.abspath(dest_dir)
    else:
        return os.path.dirname(image_path)


def main(image_args=None):
    args = get_arguments() or exit("No size arguments")
    image_path = os.path.abspath(args.image_path)
    orig_image = get_original_image(image_path) or exit("File not found")
    orig_name = os.path.basename(image_path).split(".")[0]
    orig_ext = {"JPEG": ".jpg", "PNG": ".png"}[orig_image.format]
    orig_width, orig_height = orig_image.size
    output_dir = get_output_dir(args.dest_dir, image_path)
    new_size = get_new_size(
        *orig_image.size,
        args.width,
        args.height,
        args.scale,
    ) or exit("Wrong aspect_ratio")
    new_image = get_scaled_image(orig_image, new_size)
    new_name = get_new_name(
        args.dest_dir,
        orig_name,
        *new_size,
        orig_ext,
    )
    if save_image(new_image, output_dir, new_name):
        print("Saved")
    else:
        exit("File exists")


if __name__ == "__main__":
    main()
