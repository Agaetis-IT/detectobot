import os
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from config import params
from PIL import Image

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = "{}/{}".format(params["model.dir"], params["model.name"])

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = "{}/{}".format(params["model.dir"], params["model.label"])

NUM_CLASSES = params["model.nClasses"]

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    return sess.run([boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

def getImage(inputPath):
    path = os.path.join(params["file.location"] + inputPath)
    image = Image.open(path)
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

def bubbleSort(tab):
    #We reverse the list "tableau" because it the list we want to sort is often in a decreasing order, 
    #and the bubble sort is more efficient when the list is in a increasing order
    tab.reverse()
    swapping = True
    step = 0
    while swapping == True:
        swapping = False
        step = step + 1
        for current in range(0, len(tab) - step):
            if tab[current]["score"] > tab[current + 1]["score"]:
                swapping = True
                tab[current], tab[current + 1] = \
                tab[current + 1],tab[current]
    tab.reverse()
    return tab  

def formatDetectionOutput(scores, boxes, labels):
    list_detect=[]
    detect={}
    for s_class, b_class, l_class in zip(scores, boxes, labels):
        for score, box, label in zip(s_class, b_class, l_class):
            detect["score"]=score.tolist()
            detect["box"]={params["output.ymin"]:float(box[0]), params["output.xmin"]:float(box[1]), params["output.ymax"]:float(box[2]), params["output.xmax"]:float(box[3])}
            detect["label"]=category_index[int(label)]['name']
            list_detect.append(detect.copy())
    bubbleSort(list_detect)
    return list_detect

def worker(input_q, output_q):
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
        tf.logging.set_verbosity(-1)

    while True:
        image = input_q.get()
        image[params['output.detectionError']] = ""
        if os.path.exists(params['file.location'] + image[params['input.path']]):
            (boxes, scores, classes, num_detections) = detect_objects(getImage(image[params['input.path']]), sess, detection_graph)
            image[params['output.detection']] = formatDetectionOutput(scores, boxes, classes)
        else:
            image[params['output.detectionError']] = "Incorrect path {}".format(image[params['input.path']])
        output_q.put(image)

    sess.close()
