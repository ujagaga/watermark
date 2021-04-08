#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import PySimpleGUI as sg

STAMP = "My watermark text"
FONT_NAME = "Vidaloka-Regular.ttf"
ACCEPT_TYPE = ['jpg', 'jpeg', 'png']


def get_max_font_size(w, h):
    maxw = w
    if w > h:
        maxw = h

    # Calculate starting font size
    font_size = int(maxw/len(STAMP))

    # Calculate text width
    font = ImageFont.truetype(FONT_NAME, font_size)
    text_w, text_h = font.getsize(STAMP)

    # Calculate needed font size to achieve requested width
    ratio = maxw/text_w
    font_size = int(font_size * ratio) - 2

    return font_size


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def generate_stamp(w, h):
    font_size = get_max_font_size(w, h)
    font = ImageFont.truetype(FONT_NAME, font_size)
    text_w, text_h = font.getsize(STAMP)

    c_text = Image.new('RGBA', (text_w, text_h), color=(0, 0, 0, 0))
    drawing = ImageDraw.Draw(c_text)
    drawing.text((0, 0), STAMP, fill="#ffffff", font=font)
    #c_text.putalpha(50)    
    # Crop image to loose top edge
    c_text = c_text.crop((0, int(text_h/5), text_w, text_h))
    c_text = reduce_opacity(c_text, 0.3)

    # rot = c_text.rotate(45, expand=1)

    return c_text


def copyright_apply(input_image_path, output_image_path):
    photo = Image.open(input_image_path)

    # Store image width and height
    w, h = photo.size

    # generate stamp
    stamp = generate_stamp(w, h)
    sw, sh = stamp.size

    photo.paste(stamp, (int((w - sw)/2), int((h - sh)/2)), stamp)
    photo.save(output_image_path)


src = sg.popup_get_file('Izaberi sliku', multiple_files=True, no_window=True, file_types=(('image files', '.jpeg',), ('image files', '.jpg',), ('image files', '.png',),))

for image in src:
    try:
        if image.split('.')[-1] in ACCEPT_TYPE:
            dst_dir = os.path.dirname(image)
            src_name = os.path.basename(image).split('.')
            dst_name = src_name[0] + '_stamped.' + src_name[1]
            dst = os.path.join(dst_dir, dst_name)

            copyright_apply(image, dst)
            print("Stamped: ", image)
    except Exception as e:
        print("ERR: {}".format(e))

