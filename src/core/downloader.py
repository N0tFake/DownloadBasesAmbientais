import ssl
import certifi
import mimetypes
from urllib.request import urlretrieve, urlopen
from pathlib import Path
from tqdm import tqdm
import requests


#! WARNING
ssl._create_default_https_context = ssl._create_unverified_context
""""
Se estiver usando um ambiente Python gerenciado (como Conda ou virtualenv), atualize os certificados com:
>>  pip install --upgrade certifi

USE:

context = ssl.create_default_context(cafile=certifi.where())
with urlopen(url, context=context) as response:
    content_type = response.headers.get("Content-Type")
    print(f"Content-Type: {content_type}")
"""

# TODO Obter os links de download dos arquivos
file_name = "teste.zip"


# def get_mine_type(file_name):
#     mimetype = mimetypes.guess_extension(file_name)
#     return mimetype4


# with urlopen(url) as response:
#     content_type = response.headers.get("Content-Type")
#     print(f"Content-Type: {content_type}")

# path, headers = urlretrieve(url, file_name)

# print(f"Type file: {get_mine_type(file_name)}")

# for name, value in headers.items():
#   print(f"{name}: {value}")
  
class Downloader:
    def download(self, url, file_name, file_path):
        output = Path(file_path).joinpath(file_name)
        try:
            response = requests.get(url, stream=True, verify=False)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            progress_bar = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                desc=f"Baixando {file_name}",
                leave=True
            )
            
            with open(output, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
            
            progress_bar.close()
            
            return {
                'success': True,
                'path': str(output),
                'header': dict(response.headers)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }