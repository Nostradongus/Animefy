"""
Freezes a model's graph based on current checkpoint meta.

Last updated: 05/24/22
"""

import tensorflow.compat.v1 as tf

# model checkpoint folders per anime style
ckpt_folders = ['AnimeGANv2/checkpoint/generator_Paprika_weight',
                'AnimeGANv2/checkpoint/generator_Shinkai_weight',
                'AnimeGANv2/checkpoint/generator_Hayao_weight']

# the checkpoint meta files per anime style
meta_files = ['Paprika-98.ckpt.meta', 'Shinkai-53.ckpt.meta', 'Hayao-99.ckpt.meta']

# output model filenames per anime style
output_files = ['Paprika.pb', 'Shinkai.pb', 'Hayao.pb']

for i in range(len(meta_files)):
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # restore the graph
        saver = tf.train.import_meta_graph(ckpt_folders[i] + '/' + meta_files[i])
        
        # load the weights
        saver.restore(sess, tf.train.latest_checkpoint(ckpt_folders[i]))
        
        output_node_names = [n.name for n in tf.get_default_graph().as_graph_def().node]
        
        # freeze the graph
        frozen_graph_def = tf.graph_util.convert_variables_to_constants(
            sess,
            sess.graph_def,
            output_node_names
        )
        
        # save the frozen graph for current anime style
        with open(output_files[i], 'wb') as f:
            f.write(frozen_graph_def.SerializeToString())
            
        sess.close()