from datetime import datetime
from pathlib import Path
import sqlite3
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import project_routes
from src.config.logger_config import LoggerConfig
from src.core.Validations import Validations
from src.core.downloader import Downloader
from src.utils.check_link import CheckLink


class Processor:
    def __init__(self, process_name: str, data_sources: dict, track_changes: bool = False):
        
        self.process_name = process_name.lower()
        self.data_sources = data_sources
        self.track_changes = track_changes
                
        # Configurações
        self.routes = project_routes.Routes(process_name.capitalize())
        self.logger_config = LoggerConfig()
        self.logger = self.logger_config.get_logger()
    
        self.downloader = Downloader()
        self.validation = Validations()
        
        # Estado da execução atual (para relatório em memória)
        self.current_execution_data = []
        
        # Configurações específicas de histórico
        if self.track_changes:
            # Verifica se está em modo teste
            load_dotenv()
            modo_teste = os.getenv('TESTE', '').lower() == 'true'
            suffix = '_teste' if modo_teste else ''
            
            self.database_path = self.routes.project_path() / f"{self.process_name}_database{suffix}.db"
            self._init_database()
        else:
            self.database_path = None

    def _init_database(self):
        """Inicializa o banco de dados SQLite (Apenas se track_changes=True)."""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    orgao TEXT NOT NULL,
                    dataset_slug TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    download_date TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    is_shapefile BOOLEAN NOT NULL,
                    previous_hash TEXT,
                    hash_changed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            self.logger.info(f"Banco de dados para {self.process_name} inicializado.")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar banco de dados: {e}")

    async def validate_links(self) -> Dict[str, bool]:
        """Valida todos os links das fontes de dados."""
        self.logger.info(f"[{self.process_name.upper()}] Iniciando validação de links...")
        results = {}
        
        for orgao, source in self.data_sources.items():
            for dataset in source.datasets:
                for idx, url in enumerate(dataset.urls):
                    key = f"{orgao.value}_{dataset.slug}_{idx}"
                    try:
                        check_link = await CheckLink.create(url)
                        results[key] = check_link.is_valid
                        
                        if check_link.is_valid:
                            self.logger.info(f"✓ Link válido: {url}")
                        else:
                            self.logger.warning(f"✗ Link inválido: {url} - {check_link.error_message}")
                    except Exception as e:
                        self.logger.error(f"Erro ao validar {url}: {e}")
                        results[key] = False
        return results

    async def download_data(self) -> Dict[str, List[Dict]]:
        """Realiza o download e processamento condicional (hash/db)."""
        self.logger.info(f"[{self.process_name.upper()}] Iniciando downloads...")
        download_results = {}
        self.current_execution_data = [] # Limpa dados da execução anterior

        for orgao, source in self.data_sources.items():
            orgao_results = []
            output_path = self.routes.get_output_path(source.name)
            self.logger.info(f"Processando órgão: {source.name}")
            
            for dataset in source.datasets:
                dataset_result = {
                    'slug': dataset.slug,
                    'downloads': [],
                    'success': False
                }
                
                for url in dataset.urls:
                    # 1. Validação link
                    check_link = await CheckLink.create(url)
                    if not check_link.is_valid:
                        continue
                    
                    # 2. Download
                    result = self.downloader.download(url=url, file_name=dataset.file_name, file_path=output_path)
                    
                    if result['success']:
                        file_path = Path(result['path'])
                        is_shapefile = self._check_shapefile(file_path)
                        file_size = file_path.stat().st_size
                        
                        file_hash = None
                        hash_changed = None
                        previous_hash = None

                        if self.track_changes:
                            file_hash = self._calculate_file_hash(file_path)
                            previous_hash = self._get_previous_hash(orgao.value, dataset.slug)
                            hash_changed = (previous_hash != file_hash) if previous_hash else True
                            
                            # Salvar no DB
                            self._save_download_info({
                                'orgao': orgao.value,
                                'dataset_slug': dataset.slug,
                                'file_name': dataset.file_name,
                                'file_path': str(file_path),
                                'file_hash': file_hash,
                                'file_size': file_size,
                                'is_shapefile': is_shapefile,
                                'previous_hash': previous_hash,
                                'hash_changed': hash_changed
                            })

                        download_info = {
                            'orgao': orgao.value,
                            'dataset': dataset.slug,
                            'url': url,
                            'path': str(file_path),
                            'is_shapefile': is_shapefile,
                            'file_size': file_size,
                            'hash': file_hash if self.track_changes else "N/A",
                            'hash_changed': hash_changed if self.track_changes else False
                        }
                        
                        dataset_result['downloads'].append(download_info)
                        dataset_result['success'] = True
                        self.current_execution_data.append(download_info)
                        
                        self.logger.info(f"✓ Sucesso: {dataset.slug}")
                        if self.track_changes:
                            self.logger.info(f"- Alterado: {hash_changed}")
                        
                        break # Parar na primeira URL que funciona
                    
                    else:
                        self.logger.error(f"Erro download: {result.get('error')}")

                orgao_results.append(dataset_result)
            download_results[orgao.value] = orgao_results
            
        return download_results

    def generate_report(self) -> Dict:
        total = len(self.current_execution_data)
        valid_shapes = sum(1 for d in self.current_execution_data if d['is_shapefile'])
        changed = sum(1 for d in self.current_execution_data if d.get('hash_changed', False))
        
        report = {
            'process': self.process_name,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'mode': 'Historical/DB' if self.track_changes else 'Simple Download',
            'summary': {
                'total_downloads': total,
                'valid_shapefiles': valid_shapes,
            },
            'downloads': self.current_execution_data
        }
        
        if self.track_changes:
            report['summary']['changed_files'] = changed
            
        return report

    def print_report(self, report: Dict):
        print("\n" + "="*80)
        print(f"RELATÓRIO: {report['process'].upper()} - {report['date']}")
        print(f"Modo: {report['mode']}")
        print("="*80)
        
        s = report['summary']
        print(f"📊 RESUMO:")
        print(f"   • Total Downloads: {s['total_downloads']}")
        print(f"   • Shapefiles Válidos: {s['valid_shapefiles']}")
        if self.track_changes:
            print(f"   • Arquivos Alterados: {s['changed_files']}")
            
        print(f"\n📋 DETALHES:")
        for d in report['downloads']:
            status_shape = "✓" if d['is_shapefile'] else "✗"
            size_mb = d['file_size'] / (1024 * 1024)
            
            line = f"   {status_shape} {d['orgao']:<12} | {d['dataset']:<30} | {size_mb:.1f}MB"
            
            if self.track_changes:
                status_change = "🔄" if d['hash_changed'] else "➖"
                line += f" | {status_change}"
            
            print(line)
        print("="*80)

    # --- Métodos Auxiliares ---
    def _check_shapefile(self, file_path: Path) -> bool:
        try:
            return self.validation.is_shapefile(str(file_path))
        except Exception:
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        try:
            return self.validation.get_hash_file(str(file_path))
        except Exception:
            return ""

    def _get_previous_hash(self, orgao: str, dataset_slug: str) -> Optional[str]:
        if not self.database_path: return None
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT file_hash FROM downloads 
                WHERE orgao = ? AND dataset_slug = ? 
                ORDER BY created_at DESC LIMIT 1
            ''', (orgao, dataset_slug))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except Exception:
            return None

    def _save_download_info(self, info: Dict):
        if not self.database_path: return
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO downloads (
                    orgao, dataset_slug, file_name, file_path, download_date,
                    file_hash, file_size, is_shapefile, previous_hash, hash_changed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                info['orgao'], info['dataset_slug'], info['file_name'], info['file_path'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                info['file_hash'], info['file_size'], info['is_shapefile'],
                info['previous_hash'], info['hash_changed']
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Erro ao salvar no DB: {e}")

    async def run(self):
        """Orquestrador principal."""
        try:
            self.logger.info(f"🚀 Iniciando processo {self.process_name}...")
            
            await self.validate_links()
            await self.download_data()
            
            report = self.generate_report()
            self.print_report(report)
            
            self.logger_config.export_log(prefix=f"{self.process_name}_completo")
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Erro fatal em {self.process_name}: {e}")
            raise
    