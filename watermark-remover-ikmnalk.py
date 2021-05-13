import os
import sys

import cv2


def remove_watermark(input, output):
    src = cv2.imread(input)
    width, height = src.shape[:2]

    if(width> height):
        mask = cv2.imread('ikmanlk_masks/mask-ver.png', cv2.IMREAD_GRAYSCALE)
    else:
        mask = cv2.imread('ikmanlk_masks/mask-hori.png', cv2.IMREAD_GRAYSCALE)

    resized = cv2.resize(mask, (height,width),interpolation=cv2.INTER_LINEAR)

    dst = cv2.inpaint(src, resized, 3, cv2.INPAINT_NS)

    new_dst = cv2.inpaint(dst, resized, 9, cv2.INPAINT_TELEA)

    cv2.imwrite(output, new_dst)

    print('one waternmark removed...')


def main():
    dir_name = ""
    if len(sys.argv) > 1:
        dir_name = sys.argv[1]

    dir = f"scraped_images/{dir_name}"
    output_dir = f"scraped_images/{dir_name}_watermark_removed"
    filelist = []

    try:
        for root, dirs, files in os.walk(dir):
            for file in files:
                filelist.append(os.path.join(root,file))

        for photo in filelist:
            out = photo.replace(dir, output_dir)
            get_dir = "/".join(out.split("/")[0:4])
            if not os.path.exists(get_dir):
                os.makedirs(get_dir)
            remove_watermark(photo,out)
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    main()