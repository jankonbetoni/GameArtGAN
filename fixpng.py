import os
import PIL
print(PIL.__version__)
from PIL import Image
from shutil import copyfile
import shutil

#for item in os.listdir('dc'):
#  if isfile(obj):
#            print obj
#        elif isdir(obj)
#  print(item)
#	image = PIL.Image.open(item).convert('RGBA')
#  image.save()

shutil.rmtree('dcfixed')
os.mkdir('dcfixed')

def remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg.convert('RGB')

    else:
        return im

for root, dirs, files in os.walk("./dc"):
	for name in dirs:
		os.mkdir(os.path.join(root.replace('dc', 'dcfixed'), name))
	for name in files:
		if not name.split('.')[-1] == 'png':
			copyfile(os.path.join(root, name), os.path.join(root.replace('dc', 'dcfixed'), name))
		else:
			image = Image.open(os.path.join(root, name))
			#png.load() # required for png.split()

			#background = Image.new("RGB", png.size, (255, 255, 255))
			#background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

			#background.save('foo.jpg', 'JPEG', quality=80)
			image = remove_transparency(image)
			image.save(os.path.join(root.replace('dc', 'dcfixed'), name), 'PNG')


