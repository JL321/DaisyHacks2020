import keywords
import os
from fuzzywuzzy import process
from google.cloud import vision
import io
def find_prodname_and_org(string, prod2cased):
    '''returns a tuple in the form of (cased_string, organic)
    '''
    org = 0
    good_words = []
    for each in string.lower().split():
        if each in keywords.title_words:
            good_words.append(each)
    if "organic" in good_words:
        org = 1
    string = " ".join(good_words)
    print(string)
    top_token = process.extract(string, list(prod2cased.keys()))
    if top_token:
        return (prod2cased[top_token[0][0]], org)
    else:
        return ("", org)

def fetch_text(path):
    """Detects text in the file. returns a string"""
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

if __name__ == "__main__":
    path = "C:/Users/runze/OneDrive/Desktop/DaisyHacks2020/sampleImages/week_1_page_1_prod_1.jpg"
    os.system("set GOOGLE_APPLICATION_CREDENTIALS=C:/Users/runze/OneDrive/Desktop/textdetector-f1de5e1e531e.json")
    print(fetch_text(path))