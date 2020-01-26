from darkflow.net.build import TFNet
import cv2
import os

def segmentImages(imgDir='ad_data/flyer_images-20200125T164828Z-001/flyer_images',
                  confidence=0.2):

    options = {"model": "cfg/yolov2-voc-1c.cfg",
               "load": 318,
               'threshold': 0.4,
               'gpu': 0.9}

    tfnet = TFNet(options)

    files = os.listdir(imgDir)

    for file in files:
        newDir = os.path.join(imgDir, file[:-3])
        if os.path.isdir(newDir) is False:
            os.mkdir(newDir)  # Create new directory
        imgPath = os.path.join(imgDir, files)
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = tfnet.return_predict(img)  # Return dict of predictions

        cropC = 0
        for block in result:
            if block['confidence'] > confidence:
                tlx, tly = block['topleft'].values()
                brx, bry = block['bottomright'].values()

                cropRegion = img[tlx:brx][bry:tly][:]
                #  Define new file path
                fileName = file[:-3]+'_c{}.jpg'.format(cropC)
                filePath = os.path.join(newDir, fileName)
                cv2.imwrite(filePath, cropRegion)
                cropC += 1
