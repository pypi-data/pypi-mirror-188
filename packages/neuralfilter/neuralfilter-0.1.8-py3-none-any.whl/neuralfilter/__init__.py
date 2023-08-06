import numpy as np
import tensorflow as tf
import neuralfilter.utils as utils
import neuralfilter.attention as attn

def gpu_by_growth():

    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)

def generate(x, force=False):

    assert len(x.shape) == 3
    if(force):
        if(x.shape[-1] > 1):
            x = np.expand_dims(np.average(x, axis=-1), axis=-1)
    else:
        assert x.shape[-1] == 1

    x = np.expand_dims(utils.min_max_norm(x), axis=0)

    dic_mat = attn.get_weight()
    list_key = list(dic_mat.keys())
    list_key_w = []
    for name_key in list_key:
        if('_w' in name_key):
            list_key_w.append(name_key)

    for name_key in list_key_w:

        if('clf' in name_key): break

        w = dic_mat[name_key]
        b = dic_mat[name_key.replace('_w', '_b')]

        x = tf.nn.conv2d(x, w, strides=1, padding='SAME')
        x += b

        if('conv' in name_key):
            x = tf.nn.relu(x)
        elif('attn' in name_key):
            n, h, w, c = x.shape
            x = tf.reshape(x, (n, -1))
            x = tf.nn.softmax(x, axis=1)
            x = tf.reshape(x, (n, h, w, c))

        if('conv2' in name_key):
            x = tf.nn.max_pool2d(x, ksize=2, strides=2, padding='VALID')

    return utils.zoom(x[0], ratio=[4, 4, 1])

def batch_generate(x, force=False):

    assert len(x.shape) == 4
    if(force):
        if(x.shape[-1] > 1):
            x = np.expand_dims(np.average(x, axis=-1), axis=-1)
    else:
        assert x.shape[-1] == 1

    x = utils.min_max_norm(x)

    dic_mat = attn.get_weight()
    list_key = list(dic_mat.keys())
    list_key_w = []
    for name_key in list_key:
        if('_w' in name_key):
            list_key_w.append(name_key)

    for name_key in list_key_w:

        if('clf' in name_key): break

        w = dic_mat[name_key]
        b = dic_mat[name_key.replace('_w', '_b')]

        x = tf.nn.conv2d(x, w, strides=1, padding='SAME')
        x += b

        if('conv' in name_key):
            x = tf.nn.relu(x)
        elif('attn' in name_key):
            n, h, w, c = x.shape
            x = tf.reshape(x, (n, -1))
            x = tf.nn.softmax(x, axis=1)
            x = tf.reshape(x, (n, h, w, c))

        if('conv2' in name_key):
            x = tf.nn.max_pool2d(x, ksize=2, strides=2, padding='VALID')

    return utils.zoom(x, ratio=[1, 4, 4, 1])
