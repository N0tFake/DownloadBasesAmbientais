import logging
import datetime
from pathlib import Path
from project_routes import Routes
from rich.logging import RichHandler

class MemoryHandler(logging.Handler):
    def __init__(self, log_storage):
        super().__init__()
        self.log_storage = log_storage
    
    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_storage.append(msg)
        except Exception:
            self.handleError(record)

class LoggerConfig():
  def __init__(self, name="GetBasesEmbargos", sub_name=None, level=logging.INFO):
    self.name = f"{name}.{sub_name}" if sub_name else name
    self.str_formatter = '[%(asctime)s] %(name)s - %(levelname)s: %(message)s'
    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(level)

    self.log_messages = []
    if not self.logger.hasHandlers():  
      self.log_formatter = logging.Formatter(self.str_formatter)
      
      # RichHandler para output rico no console
      console_handler = RichHandler(
          rich_tracebacks=True,
          markup=True,
          show_time=True,
          show_level=True,
          show_path=True, 
          omit_repeated_times=False
      )
      console_handler.setLevel(level)
      console_handler.setFormatter(self.log_formatter)
      self.logger.addHandler(console_handler)

      memory_handler = MemoryHandler(self.log_messages)
      memory_handler.setLevel(level)
      memory_handler.setFormatter(self.log_formatter)
      self.logger.addHandler(memory_handler)
    
    else:
      for handler in self.logger.handlers:
        if isinstance(handler, MemoryHandler):
          self.log_messages = handler.log_storage
          break
        else:
          self.__recover_memory_handler()

  def __recover_memory_handler(self):
    for handler in self.logger.handlers:
      if isinstance(handler, MemoryHandler):
        self.log_messages = handler.log_storage
        break
      else:
        memory_handler = MemoryHandler(self.log_messages)
        memory_handler.setLevel(self.logger.level)
        memory_handler.setFormatter(logging.Formatter(self.str_formatter))
        self.logger.addHandler(memory_handler)

  def get_logger(self):
    return self.logger
  
  def export_log(self, prefix="log"):
    now = datetime.datetime.now()
    filename = f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    
    log_path = Path(Routes().log_path())
    log_path.mkdir(parents=True, exist_ok=True)
    
    file_path = log_path / filename
    
    try:
      with open(file_path, "w", encoding="utf-8") as f:
        if self.log_messages:
          for message in self.log_messages:
            f.write(message + "\n")
        else:
          f.write(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] No log messages found.\n")
      self.logger.info(f"Log exported successfully to: {file_path}")
      
    except Exception as e:
      self.logger.error(f"Failed to export log: {e}")
      return None
    
    return filename

  def clear_log_memory(self):
    self.log_messages.clear()
    