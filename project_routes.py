from datetime import datetime, timedelta
import os
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.absolute()
DOWNLOADS_ROOT = Path(r'C:\Users\silvio.chaves\Desktop\MAIN\Atualizações de Bases\Embargos')

class Routes:
  
  def project_path(self):
    return PROJECT_PATH
  
  def log_path(self):
    return os.path.join(PROJECT_PATH, "logs")
  
  def data_path(self):
    return os.path.join(PROJECT_PATH, "data")
  
  def get_output_path(self, embargo_name, day_offset=0):
    month_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }

    base_path = DOWNLOADS_ROOT.joinpath(embargo_name)
    current_date = datetime.now() + timedelta(days=day_offset)

    day = current_date.strftime("%d")
    month = month_map[int(current_date.strftime("%m"))]
    year = current_date.strftime("%Y")

    output_path = base_path.joinpath(year, month, day)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
  
  def get_existing_path(self, embargo_name, day_offset=-1):
    month_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    
    base_path = Path(r'C:\Users\silvio.chaves\Desktop\MAIN\Atualizações de Bases\Embargos').joinpath(embargo_name)
    
    current_date = datetime.now() + timedelta(days=day_offset)
    
    max_attempts = abs(day_offset) + 60
    attempts = 0
    
    while attempts < max_attempts:  
      day = current_date.strftime("%d")
      month = month_map[int(current_date.strftime("%m"))]
      year = current_date.strftime("%Y")
      
      candidate_path = base_path.joinpath(year, month, day)
      if candidate_path.exists():
        return candidate_path
      
      current_date -= timedelta(days=1)
      attempts += 1

    return None 
  
  def get_output_path_manual(self, embargo_name, day_offset=0):
    return self.get_existing_path(embargo_name, day_offset)

  def log_hash_comparete(self):
    return os.path.join(self.log_path(), "hash_comparete.log")