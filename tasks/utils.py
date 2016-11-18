
import os
from django.core.files.storage import default_storage
from PIL import Image, ImageOps, ImageEnhance
from myp2.settings import STATIC_ROOT, MEDIA_ROOT
import multiprocessing

APPLY_WATERMARK = True;
PATCH_TO_WATERMARK = os.path.join(STATIC_ROOT, 'img/watermark_logo_2line.png'); 
ASPECT_RATIO_X = 1; 
ASPECT_RATIO_Y = 1; 



def reduce_opacity(im, opacity):

    assert 0 <= opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def overlay_watermark(obj_img_model, prev_params):
    img_origin = Image.open(obj_img_model.image)
    if (img_origin.size[0]/ASPECT_RATIO_X) != (img_origin.size[1]/ASPECT_RATIO_Y):
        if (img_origin.size[0]/ASPECT_RATIO_X) > (img_origin.size[1]/ASPECT_RATIO_Y):
            white_bg_size = (int(img_origin.size[0]), (int(img_origin.size[0]/ASPECT_RATIO_X)*ASPECT_RATIO_Y))
        else:
            white_bg_size = (int((img_origin.size[1]/ASPECT_RATIO_Y)*ASPECT_RATIO_X), int(img_origin.size[1]))
        white_background = Image.new('RGBA', white_bg_size, 'white')
        white_background.paste( img_origin, (int((white_bg_size[0] - img_origin.size[0]) / 2), int((white_bg_size[1] - img_origin.size[1]) / 2)))
        img_origin = white_background
    img_name =  str(obj_img_model.image).split('/')[-1]
    for prev_param in prev_params:
        img_preview = img_origin.copy()
        wtm_preview = prev_param['wtm'].copy()
        img_preview.thumbnail(prev_param['size'], Image.ANTIALIAS)
        wtm_preview.thumbnail(prev_param['size'], Image.ANTIALIAS)
        if img_preview.size != prev_param['size']:
            preview_background = Image.new('RGBA', prev_param['size'], 'white')
            preview_background.paste(img_preview, (int((preview_background.size[0] - img_preview.size[0]) / 2), int((preview_background.size[1] - img_preview.size[1]) / 2)))
            img_preview = preview_background
        img_preview.paste(wtm_preview, (0,0), wtm_preview)
        preview_path = os.path.join( 'image', prev_param['dir_name'], img_name)
        img_preview_file = default_storage.open(preview_path, 'w')
        img_preview.save(img_preview_file, 'JPEG', optimize=True, progressive=True)
        img_preview_file.close()
    return None

def make_previews_img_models(img_obj=None, img_objects=None):
    if APPLY_WATERMARK:
      watermark_origin = Image.open(PATCH_TO_WATERMARK)
    prev_params = [
      {'dir_name':'1024x768', 'size':(1024, 1024), 'wtm':reduce_opacity(watermark_origin, 1)},
      {'dir_name':'400x300', 'size':(400, 400), 'wtm':reduce_opacity(watermark_origin, 1)}, 
      {'dir_name':'180x135', 'size':(180, 180), 'wtm':reduce_opacity(watermark_origin, 1)}, 
      ]
    if not os.path.exists(os.path.join(MEDIA_ROOT, 'image/1024x768' )): os.makedirs(os.path.join(MEDIA_ROOT, 'image/1024x768'))
    if not os.path.exists(os.path.join(MEDIA_ROOT, 'image/400x300' )): os.makedirs(os.path.join(MEDIA_ROOT, 'image/400x300'))
    if not os.path.exists(os.path.join(MEDIA_ROOT, 'image/180x135' )): os.makedirs(os.path.join(MEDIA_ROOT, 'image/180x135'))
    if img_obj:
        overlay_watermark(img_obj, prev_params)
    if img_objects:
        count = img_objects.count()
        counter = 0
        for img_obj in img_objects:
            counter += 1
            print(str(counter) + '/' + str(count) + ' - ' + str(img_obj.image))
            p = multiprocessing.Process(target=overlay_watermark,  args=(img_obj, prev_params))
            p.start()
            p.join(0.3)
    return None