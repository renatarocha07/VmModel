from ultralytics import YOLO
import cv2
import os

# Carrega modelo YOLO
model = YOLO(os.path.join("models", "best.pt"))

def detect_objects(image_path, output_path):
    """
    Roda o modelo YOLO na imagem e salva resultado.
    Retorna:
        main_class: classe com maior confiança
        precisao: valor de confiança da main_class
    """
    results = model(image_path)  # roda detecção

    main_class = None
    max_confidence = 0.0

    for r in results:
        annotated = r.plot()  # imagem com bounding boxes
        cv2.imwrite(output_path, annotated)

        # Analisa resultados
        for box in r.boxes:
            cls = r.names[int(box.cls[0])]  # nome da classe
            conf = float(box.conf[0])       # confiança
            if conf > max_confidence:
                max_confidence = conf
                main_class = cls

    return main_class, max_confidence
