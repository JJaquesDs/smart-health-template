from pathlib import Path
import tensorflow as tf
from tensorflow.keras.models import load_model

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
MODEL_DIR = Path(__file__).resolve().parents[2] / 'lm'
# Somente inferência: os objetos de treinamento não são necessários.
model = load_model(MODEL_DIR / 'model_vgg_mod.h5', compile=False)
