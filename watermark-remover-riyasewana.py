import os
import sys

import cv2


def remove_watermark(input, output, hori_masks, ver_masks):
    src = cv2.imread(input)
    width, height = src.shape[:2]

    final_dist = None

    if(width> height):
        mask_list = ver_masks
    else:
        mask_list = hori_masks

    for mask_item in mask_list:
        mask = cv2.imread(mask_item, cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(mask, (height,width),interpolation=cv2.INTER_LINEAR)
        dst = cv2.inpaint(src, resized, 3, cv2.INPAINT_NS)
        final_dist = cv2.inpaint(dst, resized, 9, cv2.INPAINT_TELEA)

    cv2.imwrite(output, final_dist)
    print("one watermark removed...")


def main():
    dir_name = ""
    if len(sys.argv) > 1:
        dir_name = sys.argv[1]

    dir = f"scraped_images/{dir_name}"
    output_dir = f"scraped_images/{dir_name}_watermark_removed"
    filelist = []

    # mask lists
    hori_dir="riyasewana_masks/hori"
    ver_dir = "riyasewana_masks/ver"
    hori_masks=[]
    ver_masks=[]

    try:
        for root, dirs, files in os.walk(dir):
            for file in files:
                filelist.append(os.path.join(root,file))

        for root, dirs, files in os.walk(hori_dir):
            for file in files:
                hori_masks.append(os.path.join(root,file))

        for root, dirs, files in os.walk(ver_dir):
            for file in files:
                ver_masks.append(os.path.join(root,file))

        for photo in filelist:
            out = photo.replace(dir, output_dir)
            get_dir = "/".join(out.split("/")[0:4])
            if not os.path.exists(get_dir):
                os.makedirs(get_dir)
            remove_watermark(photo,out, hori_masks, ver_masks)
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    main()