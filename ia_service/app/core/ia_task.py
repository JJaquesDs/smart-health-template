import json
from pathlib import Path
import numpy as np
from PIL import Image
from app.core.model_loader import model, MODEL_DIR
from app.core.worker import celery_app

with (MODEL_DIR / 'classes.json').open() as source:
    class_indices = json.load(source)
classes = [name for name, index in sorted(class_indices.items(), key=lambda item: item[1])]
if sorted(class_indices.values()) != list(range(len(classes))):
    raise RuntimeError('Índices de classes inválidos')


@celery_app.task(name='process_image', track_started=True)
def processamento_imagem(image_path: str, exame_id: int):
    uploads = Path('/app/uploads').resolve()
    path = Path(image_path).resolve()
    if path.parent != uploads or not path.is_file():
        raise ValueError('Imagem não encontrada no diretório de uploads')
    shape = model.input_shape
    if len(shape) != 4 or shape[-1] != 3:
        raise ValueError('Formato de entrada incompatível')
    with Image.open(path) as source:
        if source.format not in {'JPEG', 'PNG'}:
            raise ValueError('Envie uma imagem JPEG ou PNG')
        if source.width * source.height > 40_000_000:
            raise ValueError('Imagem excede o limite de resolução')
        # Mantém o pré-processamento do projeto: RGB e pixels divididos por 255.
        image = source.convert('RGB').resize((shape[2] or 244, shape[1] or 244))
        batch = np.expand_dims(np.asarray(image, dtype=np.float32) / 255.0, 0)
    probabilities = np.asarray(model.predict(batch, verbose=0))[0]
    if probabilities.shape != (len(classes),) or not np.isfinite(probabilities).all():
        raise ValueError('Saída do modelo não corresponde às classes configuradas')
    if (probabilities < 0).any() or (probabilities > 1).any():
        raise ValueError('Saída do modelo não contém probabilidades válidas')
    return {
        'exame_img_id': exame_id,
        'classe': classes[int(np.argmax(probabilities))],
        'confianca': float(np.max(probabilities)),
        'lista': probabilities.reshape(1, -1).tolist(),
        'probabilidades': dict(zip(classes, map(float, probabilities))),
    }
