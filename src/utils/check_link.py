import asyncio
import random
import aiohttp
from .compression_detector import CheckCompactedFileResponse

class CheckLink:
    def __init__(self, url: str):
        self.url = url
        self.is_valid = False
        self.is_compacted_file = False
        self.status_code = None
        self.status_message  = None
        self.error_type = None
        self.error_message = None
        
        self.request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
    @classmethod
    async def create(cls, url):
      self = cls(url)
      await self.__request()
      return self  

    async def __request(self):
        try:
            connector = aiohttp.TCPConnector(
            ssl=False, 
            limit=100,
            limit_per_host=30
            )
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(headers=self.request_headers, connector=connector, timeout=timeout) as session:
                await asyncio.sleep(random.uniform(0.5, 1.5))
                async with session.get(self.url, allow_redirects=True, ssl=False) as response:
                    self.status_code = response.status
                    self.status_message = self.__get_status_message(response.status)
                    self.is_valid = 200 <= response.status < 400
                    
                    self.is_compacted_file = await self.__check_content_type(response)        
                    
        except aiohttp.ClientConnectionError  as e:  
            self.is_valid = False
            self.error_message = f"Erro de conexão: {str(e)}"
            self.error_type = type(e)
            self.status_message = "Erro de Conexão"
            
        except aiohttp.ClientResponseError as e:
            self.is_valid = False
            self.error_message = f"Erro de resposta: {str(e)}"
            self.error_type = type(e)
            self.status_message = "Erro de Resposta"
        
        except Exception as e:
            self.is_valid = False
            self.error_message = str(e)
            self.error_type = type(e)
            self.status_message = "Erro Desconhecido"

    async def __try_get_request(self, session):
        try:
            async with session.get(
                self.url, 
                allow_redirects=True,
                ssl=False
            ) as response:
                self.status_code = response.status
                self.status_message = self.__get_status_message(response.status)
                self.is_valid = 200 <= response.status < 400
                
                if self.is_valid:
                    self.is_compacted_file = await self.__check_content_type(response)
            
        except Exception as e:
            print(f'\033[31mErro na requisição GET: {str(e)}\033[0m')
    
    async def __check_content_type(self, response):
        checkCompactedFile = CheckCompactedFileResponse(response)
        return await checkCompactedFile.is_valid()
    
    def __get_status_message(self, status_code):
        status_messages = {
            200: "OK",
            204: "No Content",
            301: "Moved Permanently",
            302: "Found",
            304: "Not Modified",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout"
        }
        
        return status_messages.get(status_code, f"Status: {status_code}")

    def result_dict(self):
        return {
            'url': self.url,
            'status_code': self.status_code,
            'status_message': self.status_message,
            'is_valid': self.is_valid,
            'is_compacted_file': self.is_compacted_file,
            'error_type': str(self.error_type) if self.error_type else None,
            'error_message': self.error_message
        }

    def is_valid_compacted_file_link(self):
        return self.is_valid and self.is_compacted_file