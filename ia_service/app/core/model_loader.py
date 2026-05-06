import tensorflow as tf
from tensorflow.keras.models import load_model

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

model = load_model("lm/model_vgg_mod.h5")



"""
TODO:

model = None  ## Caso queira usar mais de um modelo, podemos alterar a variável aqui


def load_model_start():
    global model  # Alterando a variável global

    if model is None:
        pass
    return model

"""