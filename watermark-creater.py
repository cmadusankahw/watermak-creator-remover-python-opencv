import os
import sys
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import cv2


def copyright_apply(input_image_path,
                    output_image_path,
                    text, png_mode=True):
    photo = Image.open(input_image_path)

    # Store image width and heigth
    w, h = photo.size
    # print(w, h )

    if not png_mode:
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

    else:
        if(w<h):
            x = int(0.1*w)
            y = int(0.4*h)
        else:
            x = int(0.3*w)
            y = int(0.4*h)
        overlay = cv2.imread(text, cv2.IMREAD_UNCHANGED)
        background = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)

        final_image = overlay_transparent(background=background, overlay=overlay, x=x,y=y)
        cv2.imwrite(output_image_path, final_image)

    print("one image watermarked...")


def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

def main():
    dir_name = ""
    text_name="sample"
    mode = "text"
    if len(sys.argv) > 1:
        dir_name = sys.argv[1]

    if len(sys.argv) > 2:
        mode = sys.argv[2]

    if len(sys.argv) > 3:
        text_name = sys.argv[3]

    actual_mode = True
    if "text" in mode:
        actual_mode = False
    if "logo" in mode:
        actual_mode = True

    dir = f"scraped_images/{dir_name}"
    output_dir = f"scraped_images/{dir_name}_watermarked"
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
                        text_name,
                        actual_mode)


if __name__ == "__main__":
    main()