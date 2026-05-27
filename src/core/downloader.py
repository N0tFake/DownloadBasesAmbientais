import ssl
import certifi
import mimetypes
from urllib.request import urlretrieve, urlopen
from pathlib import Path
from tqdm import tqdm
import requests
import urllib3
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)


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

# class Downloader:
#     def download(self, url, file_name, file_path):
#         output = Path(file_path).joinpath(file_name)
#         try:
#             response = requests.get(url, stream=True, verify=certifi.where())
#             response.raise_for_status()
            
#             total_size = int(response.headers.get('content-length', 0))
            
#             progress_bar = tqdm(
#                 total=total_size,
#                 unit='B',
#                 unit_scale=True,
#                 desc=f"Baixando {file_name}",
#                 leave=True
#             )
            
#             with open(output, 'wb') as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)
#                         progress_bar.update(len(chunk))
            
#             progress_bar.close()
            
#             return {
#                 'success': True,
#                 'path': str(output),
#                 'header': dict(response.headers)
#             }
#         except Exception as e:
#             return {
#                 'success': False,
#                 'error': str(e)
#             }

class Downloader:
    def download(self, url, file_name, file_path):
        output = Path(file_path).joinpath(file_name)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        try:
            response = requests.get(
                url, 
                stream=True, 
                verify=certifi.where(),
                headers=headers,     
                allow_redirects=True
            )
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                transient=True
            ) as progress:
                
                task_id = progress.add_task(f"Baixando {file_name}", total=total_size)
                
                with open(output, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task_id, advance=len(chunk))
            
            return {
                'success': True,
                'path': str(output),
                'header': dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
