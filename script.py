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
    
items=os.listdir("./pixels.deviantart.com")
giflist=[]
renamelist=[]
for filename in items:
    #print(filename)
    try:
        img = Image.open('./pixels.deviantart.com/' + filename)
        print('Format: ', img.format)  # 'JPEG'
        #if (os.path.basename(inGif)):
        #    os.path.basename(inGif)
        if img.format=="GIF":
            giflist.append('./pixels.deviantart.com/' + filename)
    except:
        pass
    
for name in giflist:
    print(name)
    extractFrames(name, './frames')

print(len(giflist))
