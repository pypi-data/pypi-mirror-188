# Python PixelPay SDK

## ¿Como instalar?
Si se quiere utilizar un ambiente virtual, referirse al siguiente [enlace](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment):
```bash
python3 -m venv env
source ./env/bin/activate
```

Por medio de PIP, agregue el SDK de PixelPay
``` bash
# MacOS / Linux
python3 -m pip install pixelpay_sdk

# Windows
py -m pip install pixelpay_sdk
```

## ¿Como publicar?
Obtenga todos los requerimientos del SDK al momento de desarrollar:
``` bash
# MacOS / Linux
python3 -m pip install -r requirements.txt

# Windows
py -m pip install -r requirements.txt
```

Luego de hacer cambios en el SDK, modificar el `CHANGELOG.md` y el archivo de versión dentro de `pixelpay/__init__.py`, publicar el paquete con los siguientes comandos:
```bash
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```
