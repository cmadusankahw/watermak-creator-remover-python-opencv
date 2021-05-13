import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def copyright_apply(input_image_path,
                    output_image_path,
                    text):
    photo = Image.open(input_image_path)

    # Store image width and heigth
    w, h = photo.size
    # print(w, h )
    # make the image editable
    drawing = ImageDraw.Draw(photo)
    black = (3, 8, 12)
    if(w<h):
        font_size = 25
    else:
        font_size = 55
    font = ImageFont.truetype("chandas1-2.ttf", font_size)

    # get text width and heigth

    text = "© " + text + " "
    text_w, text_h = drawing.textsize(text, font)

    pos = w - text_w, int(h/2 - text_h/2)

    c_text = Image.new("RGB", (text_w, (text_h)), color="#000000")
    drawing = ImageDraw.Draw(c_text)

    drawing.text((0, 0), text, fill="#ffffff", font=font)
    c_text.putalpha(100)

    photo.paste(c_text, pos, c_text)
    photo.save(output_image_path)
    print("one image watermarked...")


def main():
    dir_name = ""
    text_name="sample"
    if len(sys.argv) > 1:
        dir_name = sys.argv[1]

    if len(sys.argv) > 2:
        text_name = sys.argv[2]

    dir = f"scraped_images/{dir_name}"
    output_dir = f"scraped_images/{dir_name}_watermarked_test"
    filelist = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            filelist.append(os.path.join(root,file))

    for photo in filelist:
        out = photo.replace(dir, output_dir)
        get_dir = "/".join(out.split("/")[0:4])
        if not os.path.exists(get_dir):
            os.makedirs(get_dir)
        copyright_apply(photo,
                        out,
                        text_name)


if __name__ == "__main__":
    main()