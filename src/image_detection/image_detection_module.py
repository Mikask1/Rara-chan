
from keras.models import load_model
import numpy as np
from PIL import Image

model = load_model('src/image_detection/Furry-Detection-Model')

def predict(img : Image) -> str:
    img = img.resize((300, 300))
    img = img.convert("RGB")
    img_arr = np.array(img)

    x = np.array([img_arr])/255
    pred = model.predict(x)
    
    max_index = np.argmax(pred[0])
        
    return max_index
