import os
import PIL
print(PIL.__version__)
from shutil import copyfile

#for item in os.listdir('dc'):
#  if isfile(obj):
#            print obj
#        elif isdir(obj)
#  print(item)
#	image = PIL.Image.open(item).convert('RGBA')
#  image.save()


for root, dirs, files in os.walk("./dc", topdown=False):
	for name in dirs:
		os.mkdir(os.path.join(root, name))
	for name in files:
		if not name.split('.')[-1] == '.png':
			print(os.path.join(root.replace('dc', 'dcfix'), name)
			copyfile(os.path.join(root, name), os.path.join(root.replace('dc', 'dcfix'), name))
		else:
			image = PIL.Image.open(item).convert('RGBA')
			image.save(os.path.join(root.replace('dc', 'dcfix'), name))
