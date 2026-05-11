from datetime import datetime, timedelta
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

PROJECT_PATH = Path(__file__).parent.absolute()

CONFIG_FILE = PROJECT_PATH / 'config.json'

# Cria ou lê o arquivo de configuração
if not CONFIG_FILE.exists():
    default_config = {
        "BASE_PATH": "",
        "INSTRUCOES": "Preencha o BASE_PATH com o caminho absoluto do diretorio para os downloads."
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4)
    
    print("\n" + "="*70)
    print("⚠️  ARQUIVO DE CONFIGURAÇÃO CRIADO ⚠️".center(70))
    print("="*70)
    print(f"O arquivo '{CONFIG_FILE.name}' foi criado na raiz do projeto.")
    print("Por favor, abra-o e preencha o campo 'BASE_PATH' com o caminho")
    print("do diretório principal para salvar os downloads.")
    print("Exemplo: C:\\Users\\usuario\\Desktop\\Atualizações de Bases")
    print("="*70 + "\n")
    sys.exit(1)

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config_data = json.load(f)

base_path_str = config_data.get("BASE_PATH", "").strip()

if not base_path_str:
    print("\n" + "="*70)
    print("⚠️  CONFIGURAÇÃO INCOMPLETA ⚠️".center(70))
    print("="*70)
    print(f"O campo 'BASE_PATH' no arquivo '{CONFIG_FILE.name}' está vazio.")
    print("Por favor, preencha com o caminho do diretório principal para os downloads.")
    print("="*70 + "\n")
    sys.exit(1)

# Define caminho base de downloads a partir do config.json
_BASE_PATH = Path(base_path_str)

# Se TESTE=true no .env, adiciona '/TESTE' ao caminho
if os.getenv('TESTE', '').lower() == 'true':
    DOWNLOADS_ROOT = _BASE_PATH / 'TESTE'
else:
    DOWNLOADS_ROOT = _BASE_PATH

FOLDER_NAMES = {
  'Embargos': "Embargos",
  'Deters': "Desmatamento",
  'Alertas': "Desmatamento",
  'Terras indigenas': "Areas Protegidas"
}

class Routes:
  def __init__(self, type_base=None):
    if type_base is not None:
      self.main_folder_name = FOLDER_NAMES[type_base]
  
  def project_path(self):
    return PROJECT_PATH
  
  def log_path(self):
    return os.path.join(PROJECT_PATH, "logs")
  
  def data_path(self):
    return os.path.join(PROJECT_PATH, "data")
  
  def get_output_path(self, base_name, day_offset=0):
    month_map = {
      1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
      7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    
    # embargos_path = DOWNLOADS_ROOT.joinpath('Embargos')
    type_path = DOWNLOADS_ROOT.joinpath(self.main_folder_name)
    
    base_path = type_path.joinpath(base_name)
    current_date = datetime.now() + timedelta(days=day_offset)

    day = current_date.strftime("%d")
    month = month_map[int(current_date.strftime("%m"))]
    year = current_date.strftime("%Y")

    output_path = base_path.joinpath(year, month, day)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path