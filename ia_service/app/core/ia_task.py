import json
import numpy as np
from PIL import Image

from app.core.model_loader import model
from app.core.worker import celery_app


# Carregando os rótulos das classes
with open("lm/classes.json") as classes:
    classes_indices = json.load(classes)

# Invertendo os índices para classes (EX: 0 - Disceratoticas)
idx_to_class = {
    valor: chave for chave, valor in classes_indices.items()
}


@celery_app.task(name="process_image")
def processamento_imagem(image_path: str, exame_id: int):

    print("1 - entrou na task")
    print("Modelo carregado OK")

    image = Image.open(image_path).convert("RGB")
    print("2 - imagem aberta")

    image = image.resize((244, 244))
    print("3 - resize feito")

    img = np.array(image) / 255.0
    img = np.expand_dims(img, axis=0)
    print("4 - preprocess feito")

    print("5 - entrando no predict")

    pred = model.predict(img)

    # Pegando o índice de maior valor (maior confiança na predição)
    predicted_idx = int(np.argmax(pred))

    # Puxando a classe que foi predita
    predicted_classes = idx_to_class[predicted_idx]

    # Pegando o float de maior valor (mais confiabilidade de predição da IA)
    confianca = float(np.max(pred))

    print("Classe:", predicted_classes)
    print("Confiança:", confianca)

    return {
        "exame_img_id": exame_id,
        "classe": predicted_classes,
        "confianca": confianca,
        "lista": pred.tolist(),
    }