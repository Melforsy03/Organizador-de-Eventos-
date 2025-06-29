"""
Módulo de hashing incremental para detección de cambios (scraping_incremental.py)

Este módulo permite identificar archivos JSON que han sido modificados o añadidos recientemente.
Se basa en hashes MD5 para detectar diferencias con respecto a una versión previa persistida
en un archivo `hashes.json`.

Funciones:
- `hash_file(path)`
- `load_hashes()`
- `save_hashes(hashes)`
- `archivos_a_procesar(folder)`
"""

import os
import hashlib
import json

HASH_FILE = "hashes.json"

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f)

def archivos_a_procesar(folder):
    hashes = load_hashes()
    archivos_nuevos = []

    for file in os.listdir(folder):
        if file.endswith(".json"):
            path = os.path.join(folder, file)
            h = hash_file(path)
            if file not in hashes or hashes[file] != h:
                archivos_nuevos.append(file)
                hashes[file] = h

    save_hashes(hashes)
    return archivos_nuevos
