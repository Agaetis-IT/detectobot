import multiprocessing
from multiprocessing import Queue, Pool
from app.models.objectDetection import worker
from config import params

def RunDetection(inputs):
    """
    Apply Tensorflow Object Detection to inputs images using Monobloc chair detector model
    """

    # Set the multiprocessing logger to debug if required
    if params['multiproc.debug']:
        logger = multiprocessing.log_to_stderr()
        logger.setLevel(multiprocessing.SUBDEBUG)

    # Multiprocessing: Init input and output Queue, output Priority Queue and pool of workers
    input_q = Queue(maxsize=len(inputs))
    output_q = Queue(maxsize=len(inputs))
    pool = Pool(params["multiproc.numWorkers"], worker, (input_q,output_q))

    # Put all paths in inputs into input_q
    for image in inputs:
        input_q.put(image)

    output = []
    while True:
        if not output_q.empty():
            output.append(output_q.get())

        if len(output) == len(inputs):
            break

    pool.terminate()
    return output