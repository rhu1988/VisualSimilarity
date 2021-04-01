import tensorflow as tf
import numpy as np
import os
from PIL import Image

#load a trained classifier
#classifier = tf.keras.models.load_model('./classifier/')

class product():
    def __init__(self):
        self.image = np.zeros([1,255,255,3])
        self.cat = 'None'
        self.recommendations = []
        self.img_feature = np.zeros(8*8*2048)
    def readImage(self,address):
        img = Image.open(address).resize((255,255))
        imgdata = np.asarray(img)
        self.image = np.expand_dims(imgdata,axis=0)
    # def classify(self):
    #     # a product classifier could be used here
    #     prediction = classifier(self.image)
    #     score = tf.nn.softmax(predictions[0])
    #     classes = ['Accessories', 'Apparel', 'Footwear', 'Free', 'Home', 'Personal', 'Sporting']
    #     self.cat = classes[np.argmax(score)]
    def similarity(self,p2,method='Euclidean'):
        f1 = self.img_feature
        f2 = p2.img_feature
        if method == 'Euclidean':
            sim = np.linalg.norm(f1-f2)
        elif method == 'Cosine':
            sim = np.dot(f1,np.transpose(f2))/(np.linalg.norm(f1)*np.linalg.norm(f2))
            sim = sim[0,0]
        elif method == 'Pearson':
            coef = np.corrcoef(f1,f2)
            sim = coef[0,1]
        return sim
    def feature(self):
        self.img_feature = ResNet50Feature(self.image)

def ResNet50Feature(image):
    preprocess_input = tf.keras.applications.resnet_v2.preprocess_input
    flatten = tf.keras.layers.Flatten()
    image_size = image.shape[1:]
    image_shape = image_size
    base_model = tf.keras.applications.ResNet50V2(input_shape=image_shape,
                                              include_top=False,weights='imagenet')
    img = preprocess_input(image)
    img = base_model(img,training=False)
    img = flatten(img)
    return img.numpy()