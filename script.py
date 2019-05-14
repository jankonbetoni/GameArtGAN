import os
from PIL import Image


def extractFrames(inGif, outFolder):
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save( '%s/%s-%s.png' % (outFolder, os.path.splitext(os.path.basename(inGif))[0], nframes ) , 'PNG')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return True
    

inputdir='./pixels.deviantart.com/'
outputdir='./parentframes/'
items=os.listdir(inputdir)
giflist=[]
pnglist=[] #not used right now

for filename in items:
    #print(filename)
    try:
        img = Image.open(inputdir + filename)
        print('Format: ', img.format)
        
        if img.format=="GIF":
            giflist.append(inputdir + filename)
            
        if img.format=="PNG":
          pnglist.append(inputdir + filename) 
          if not filename.split('.')[-1] == 'png':
            img.save( outputdir + filename[0:-1] + '.png')
          else:
            img.save( outputdir + filename )
        if img.format=="JPEG":
          if not filename.split('.')[-1] == 'jpeg':
            img.save( outputdir + filename.split('.')[0:-1] + '.png')
          else:
            img.save( outputdir + filename + '.png')
          
            
            
    except:
        pass
    
for name in giflist:
    print(name)
    extractFrames(name, outputdir)
