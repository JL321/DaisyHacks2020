import argparse
from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import numpy as np

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


class blockContainer:
    
    def __init__(self, block):
        self.block_list = []
        self.block_list.append(block)
        self.internalText = []
        
    def add(self, block):
        self.block_list.append(block)
        
    def rectThresh(self, new_block, thresh=100):
        for block in self.block_list:
            if rect_distance(block, new_block) < thresh:
                self.block_list.append(new_block)
                return True
        return False

    def meshBlock(self):
        # Returns bottom left, and top right corners
        allX = []
        allY = []
        for block in self.block_list:
            bl, tr = getBox(block)
            xl, yl = bl
            xt, yt = tr
            allX.extend([xl, xt])
            allY.extend([yl, yt])
        maxX = np.max(np.array(allX))
        minX = np.min(np.array(allX))
        maxY = np.max(np.array(allY))
        minY = np.min(np.array(allY))
        return ((minX, minY), (maxX, maxY))

def fetch_text(path):
    """Detects text in the file. returns a string"""
    import io
    import os
    from google.cloud import vision
    #  Self path to json
    os.system("set GOOGLE_APPLICATION_CREDENTIALS=/home/jamesl/Downloads/textdetector-f1de5e1e531e.json")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return texts[0].description


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:

        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image

def draw_boxes_c(image, corners, color):
    
    #  Takes in as input the bottom left and top right corners
    draw = ImageDraw.Draw(image)
    
    for corner in corners:
        bl, tr = corner
        x1, y1 = bl
        x2, y2 = tr
        draw.polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)], None, color)
    return image

def getBox(bound):

    xList = []
    yList = []
    for i in range(4):
        xList.append(bound.vertices[i].x)
        yList.append(bound.vertices[i].y)
    xList = np.array(xList)
    yList = np.array(yList)
    minX = np.min(xList)
    maxX = np.max(xList)
    minY = np.min(yList)
    maxY = np.max(yList)
    return (minX, minY), (maxX, maxY)

def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def render_doc_text(filein, fileout, fileoutRef='default.jpg', thresh=500):
    image = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.BLOCK)
    draw_boxes(image, bounds, 'blue')
    if fileout != 0:
        image.save(fileoutRef)
    image = Image.open(filein)
    print(len(bounds))
    print("INIT")
    blockContainerL = []  # List of lists of box coordinates
    boundIdx1 = 0
    
    for i, cbound in enumerate(bounds): # Inefficient, but culls large boxes
        bl, tr = getBox(cbound)
        width = tr[0]-bl[0]
        height = tr[1]-bl[1]
        if height > 800 or width > 800:
            del bounds[i]
    
    while len(bounds) > 0:
        sectBool = True
        
        for container in blockContainerL:  # First compare with block containers
            if container.rectThresh(bounds[boundIdx1], thresh):
                del bounds[boundIdx1]
                sectBool = False
                break
        
        if sectBool:
            for i, boundNew in enumerate(bounds):  # Compare with all other bounds
                if boundIdx1 != i:
                    if rect_distance(bounds[boundIdx1], boundNew) < thresh:
                        newBlock = blockContainer(bounds[boundIdx1])
                        newBlock.add(boundNew)
                        blockContainerL.append(newBlock)
                        del bounds[max(boundIdx1, i)]
                        del bounds[min(boundIdx1, i)]
                        sectBool = False
                        break
                    
        if sectBool:
            blockContainerL.append(blockContainer(bounds[boundIdx1]))
            del bounds[boundIdx1]
            
    print(len(blockContainerL))
    finalBoxes = []
    for container in blockContainerL:
        finalBoxes.append(container.meshBlock())
    print("Box Length: {}".format(len(finalBoxes)))
        
    draw_boxes_c(image, finalBoxes, 'blue')
    if fileout != 0:
        image.save(fileout)
    else:
        image.show()


def rect_distance(bbox1, bbox2):

    bl1, tr1 = getBox(bbox1)
    bl2, tr2 = getBox(bbox2)
    x1, y1 = tr1 
    x1b, y1b = bl1
    x2, y2 = tr2
    x2b, y2b = bl2
    
    if intersects(bl1, tr1, bl2, tr2):
        print("test")
        return 0
    
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return dist((x1, y1b), (x2b, y2))
    elif left and bottom:
        return dist((x1, y1), (x2b, y2b))
    elif bottom and right:
        return dist((x1b, y1), (x2, y2b))
    elif right and top:
        return dist((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:             # rectangles intersect
        return 0

def intersects(bl1, tr1, bl2, tr2):
    return not (tr1[0] < bl2[0] or bl1[0] > tr2[0] or tr1[1] < bl2[1] or bl1[1] > tr2[1])

def dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt(np.square(x1-x2)+np.square(y1-y2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    render_doc_text(args.detect_file, args.out_file)
    print(fetch_text("croppedImg.jpg"))
