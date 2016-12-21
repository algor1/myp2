from django import template

register = template.Library()

@register.simple_tag
def replace_dir_in_img_url(img_url, dir_name):
    return img_url.replace('/original/', dir_name)

