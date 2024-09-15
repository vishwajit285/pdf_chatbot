# utils/annotations.py
import json
import os

ANNOTATIONS_FILE = 'data/annotations.json'

def load_annotations():
    if os.path.exists(ANNOTATIONS_FILE):
        with open(ANNOTATIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_annotation(pdf_name, annotation):
    annotations = load_annotations()
    if pdf_name in annotations:
        annotations[pdf_name].append(annotation)
    else:
        annotations[pdf_name] = [annotation]
    with open(ANNOTATIONS_FILE, 'w') as f:
        json.dump(annotations, f)
