import os
import PIL
#print(PIL.__version__)
from shutil import copyfile

#for item in os.listdir('dc'):
#  if isfile(obj):
#            print obj
#        elif isdir(obj)
#  print(item)
#	image = PIL.Image.open(item).convert('RGBA')
#  image.save()

os.mkdir('dcfixed1folder')
os.mkdir('dcfixed1folder/sprite')

for root, dirs, files in os.walk("./dc"):
	for name in files:
		if name.split('.')[-1] == 'png':
			#print('image')
			#image = PIL.Image.open(item).convert('RGB')
			copyfile(os.path.join(root, name), os.path.join(os.path.join('dcfixed1folder/sprite', name)))
