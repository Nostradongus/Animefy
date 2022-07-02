import os
import tensorflow.compat.v1 as tf
import numpy as np
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# utils.py
from utils import *

# generator.py
import generator

# stylize input image with chosen anime style
def stylize(anime_style, input_image): 
    test_real = tf.placeholder(tf.float32, [1, None, None, 3], name='test')

    with tf.variable_scope("generator", reuse=False):
        test_generated = generator.G_net(test_real).fake
    saver = tf.train.Saver()
    
    # get model checkpoint folder according to chosen anime style
    checkpoint_dir = 'models/' + anime_style

    gpu_options = tf.GPUOptions(allow_growth=True)
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, gpu_options=gpu_options)) as sess:
        # load style model and its weights
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
        saver.restore(sess, os.path.join(checkpoint_dir, ckpt_name))
        
        # load and preprocess input image as a NumPy array
        image = np.asarray(load_input_image(input_image))
        
        # stylize image
        output_image = sess.run(test_generated, feed_dict = {test_real : image})
        
        # adjust brightness of output image
        output_image = adjust_brightness_from_src_to_dst(inverse_transform(output_image.squeeze()), read_img(input_image))
        
        return output_image
