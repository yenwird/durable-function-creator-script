import base64
import requests
import json

# Configura tus credenciales y el repositorio
usuario = ''
token = ''
repo = 'durabletest'


def pushToBranch(contenido, ruta_destino):
    headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    }

    # Obtén la referencia al branch (por ejemplo, main)
    response = requests.get(
        f'https://api.github.com/repos/{usuario}/{repo}/git/ref/heads/main',
        headers=headers,
    )
    data = response.json()
    tree_sha = data['object']['sha']

    # Crea un nuevo blob con el contenido del archivo
    data = {
        "content": contenido,
        "encoding": "base64",
    }
    response = requests.post(
        f'https://api.github.com/repos/{usuario}/{repo}/git/blobs',
        headers=headers,
        json=data,
    )
    data = response.json()
    blob_sha = data['sha']

    # Crea un nuevo árbol que incluye el nuevo blob
    data = {
        "base_tree": tree_sha,
        "tree": [
            {
                "path": ruta_destino,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha,
            },
        ],
    }
    response = requests.post(
        f'https://api.github.com/repos/{usuario}/{repo}/git/trees',
        headers=headers,
        json=data,
    )
    data = response.json()
    new_tree_sha = data['sha']

    # Crea un nuevo commit que apunta al nuevo árbol
    data = {
        "message": "nuevo orquestador" + ruta_destino.replace("src/functions/", "").replace(".ts", ""),
        "tree": new_tree_sha,
        "parents": [tree_sha],
    }
    response = requests.post(
        f'https://api.github.com/repos/{usuario}/{repo}/git/commits',
        headers=headers,
        json=data,
    )
    data = response.json()
    new_commit_sha = data['sha']

    # Actualiza la referencia al branch para que apunte al nuevo commit
    data = {
        "sha": new_commit_sha,
    }
    response = requests.patch(
        f'https://api.github.com/repos/{usuario}/{repo}/git/refs/heads/main',
        headers=headers,
        json=data,
    )

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        print('Archivo subido exitosamente')
    else:
        print('Error al subir el archivo:', response.content)
    
def push(ruta_archivo, ruta_destino):
    # Lee el contenido del archivo y codifícalo en base64
    with open(ruta_archivo, 'rb') as f:
        contenido = base64.b64encode(f.read()).decode('utf-8')
        pushToBranch(contenido, ruta_destino)
