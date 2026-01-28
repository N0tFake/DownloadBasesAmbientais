from datetime import datetime, timedelta
import os
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.absolute()
DOWNLOADS_ROOT = Path(r'C:\Users\silvio.chaves\Desktop\MAIN\40_Data_Hub\Atualizações de Bases')

FOLDER_NAMES = {
  'Embargos': "Embargos",
  'Deters': "Desmatamento",
  'Alertas': "Desmatamento"
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