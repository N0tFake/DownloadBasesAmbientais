"""
Sistema integrado para download e processamento de bases de dados de embargos ambientais.

Este módulo integra todas as funcionalidades do projeto:
- Validação de links
- Download das bases de dados
- Verificação se é shapefile
- Comparação de hash com dia anterior
- Logging detalhado
"""

import asyncio
import sqlite3
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from src.config.bases_infos import EMBARGOS_DATA_SOURCES, Orgao
from src.utils.check_link import CheckLink
from src.config.logger_config import LoggerConfig
from src.core.downloader import Downloader
from src.core.Validations import Validations
from src.utils.templates import Templates
from src.utils.compression_detector import CheckCompactedFileLocal
import project_routes


class EmbargoProcessor:
    """Classe principal para processamento de embargos ambientais."""
    
    def __init__(self):
        self.routes = project_routes.Routes()
        self.logger_config = LoggerConfig()
        self.logger = self.logger_config.get_logger()
        self.templates = Templates()
        self.downloader = Downloader()
        self.validation = Validations()
        self.database_path = self.routes.project_path() / "embargo_database.db"
        
        # Inicializar banco de dados
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite."""
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
        
        self.logger.info("Banco de dados inicializado com sucesso.")
    
    async def validate_links(self) -> Dict[str, bool]:
        """
        Valida todos os links das bases de dados.
        
        Returns:
            Dict com resultado da validação para cada link
        """
        self.logger.info("Iniciando validação de links...")
        results = {}
        
        for orgao, source in EMBARGOS_DATA_SOURCES.items():
            for dataset in source.datasets:
                self.logger.info(f"Validando links para: {dataset.slug}")
                
                for idx, url in enumerate(dataset.urls):
                    try:
                        check_link = await CheckLink.create(url)
                        is_valid = check_link.is_valid
                        
                        key = f"{orgao.value}_{dataset.slug}_{idx}"
                        results[key] = is_valid
                        
                        if is_valid:
                            self.logger.info(f"✓ Link válido: {url}")
                        else:
                            self.logger.warning(f"✗ Link inválido: {url} - {check_link.error_message}")
                            
                    except Exception as e:
                        self.logger.error(f"Erro ao validar link {url}: {str(e)}")
                        results[f"{orgao.value}_{dataset.slug}_{idx}"] = False
        
        return results
    
    async def download_all_embargos(self) -> Dict[str, List[Dict]]:
        """
        Realiza o download de todas as bases de embargos.
        
        Returns:
            Dict com resultados dos downloads
        """
        self.logger.info("Iniciando processo de download de embargos...")
        self.logger.info(f"Total de fontes de dados: {len(EMBARGOS_DATA_SOURCES)}")
        
        download_results = {}
        
        for orgao, source in EMBARGOS_DATA_SOURCES.items():
            orgao_results = []
            output_path = self.routes.get_output_path(source.name)
            
            self.logger.info(f"Processando órgão: {source.name}")
            
            for dataset in source.datasets:
                self.logger.info(f"Processando dataset: {dataset.slug}")
                
                dataset_result = {
                    'slug': dataset.slug,
                    'file_name': dataset.file_name,
                    'downloads': [],
                    'success': False
                }
                
                for idx, url in enumerate(dataset.urls):
                    self.logger.info(f"Tentativa {idx + 1}: {url}")
                    
                    # Validar link antes do download
                    check_link = await CheckLink.create(url)
                    if not check_link.is_valid:
                        self.logger.warning(f"Link inválido, pulando: {url}")
                        continue
                    
                    # Realizar download
                    result = self.downloader.download(
                        url=url,
                        file_name=dataset.file_name,
                        file_path=output_path
                    )
                    
                    if result['success']:
                        file_path = Path(result['path'])
                        
                        # Verificar se é shapefile
                        is_shapefile = self._check_shapefile(file_path)
                        
                        # Calcular hash
                        file_hash = self._calculate_file_hash(file_path)
                        
                        # Obter hash anterior (se existir)
                        previous_hash = self._get_previous_hash(orgao.value, dataset.slug)
                        hash_changed = previous_hash != file_hash if previous_hash else True
                        
                        # Salvar no banco de dados
                        self._save_download_info({
                            'orgao': orgao.value,
                            'dataset_slug': dataset.slug,
                            'file_name': dataset.file_name,
                            'file_path': str(file_path),
                            'file_hash': file_hash,
                            'file_size': file_path.stat().st_size,
                            'is_shapefile': is_shapefile,
                            'previous_hash': previous_hash,
                            'hash_changed': hash_changed
                        })
                        
                        download_info = {
                            'url': url,
                            'success': True,
                            'path': str(file_path),
                            'is_shapefile': is_shapefile,
                            'hash': file_hash,
                            'hash_changed': hash_changed,
                            'file_size': file_path.stat().st_size
                        }
                        
                        dataset_result['downloads'].append(download_info)
                        dataset_result['success'] = True
                        
                        self.logger.info(f"✓ Download realizado com sucesso: {file_path}")
                        self.logger.info(f"  - É shapefile: {is_shapefile}")
                        self.logger.info(f"  - Hash: {file_hash}")
                        self.logger.info(f"  - Hash alterado: {hash_changed}")
                        
                        # Parar na primeira URL que funciona
                        break
                        
                    else:
                        self.logger.error(f"✗ Erro no download: {result['error']}")
                        dataset_result['downloads'].append({
                            'url': url,
                            'success': False,
                            'error': result['error']
                        })
                
                orgao_results.append(dataset_result)
            
            download_results[orgao.value] = orgao_results
        
        return download_results
    
    def _check_shapefile(self, file_path: Path) -> bool:
        """Verifica se o arquivo é um shapefile válido."""
        try:
            return self.validation.is_shapefile(str(file_path))
        except Exception as e:
            self.logger.error(f"Erro ao verificar shapefile {file_path}: {str(e)}")
            return False
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula o hash do arquivo."""
        try:
            return self.validation.get_hash_file(str(file_path))
        except Exception as e:
            self.logger.error(f"Erro ao calcular hash de {file_path}: {str(e)}")
            return ""
    
    def _get_previous_hash(self, orgao: str, dataset_slug: str) -> Optional[str]:
        """Obtém o hash do download anterior do mesmo dataset."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_hash FROM downloads 
            WHERE orgao = ? AND dataset_slug = ? 
            ORDER BY created_at DESC 
            LIMIT 1 OFFSET 1
        ''', (orgao, dataset_slug))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def _save_download_info(self, info: Dict):
        """Salva informações do download no banco de dados."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO downloads (
                orgao, dataset_slug, file_name, file_path, download_date,
                file_hash, file_size, is_shapefile, previous_hash, hash_changed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            info['orgao'],
            info['dataset_slug'],
            info['file_name'],
            info['file_path'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            info['file_hash'],
            info['file_size'],
            info['is_shapefile'],
            info['previous_hash'],
            info['hash_changed']
        ))
        
        conn.commit()
        conn.close()
    
    def generate_report(self) -> Dict:
        """Gera relatório dos downloads realizados."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Downloads de hoje
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            SELECT orgao, dataset_slug, file_name, is_shapefile, hash_changed, file_size
            FROM downloads 
            WHERE DATE(download_date) = ?
            ORDER BY created_at DESC
        ''', (today,))
        
        today_downloads = cursor.fetchall()
        
        # Estatísticas gerais
        cursor.execute('SELECT COUNT(*) FROM downloads WHERE DATE(download_date) = ?', (today,))
        total_today = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM downloads WHERE DATE(download_date) = ? AND is_shapefile = 1', (today,))
        shapefiles_today = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM downloads WHERE DATE(download_date) = ? AND hash_changed = 1', (today,))
        changed_today = cursor.fetchone()[0]
        
        conn.close()
        
        report = {
            'date': today,
            'summary': {
                'total_downloads': total_today,
                'valid_shapefiles': shapefiles_today,
                'changed_files': changed_today
            },
            'downloads': []
        }
        
        for download in today_downloads:
            report['downloads'].append({
                'orgao': download[0],
                'dataset': download[1],
                'file_name': download[2],
                'is_shapefile': bool(download[3]),
                'hash_changed': bool(download[4]),
                'file_size': download[5]
            })
        
        return report
    
    def print_report(self, report: Dict):
        """Imprime relatório formatado."""
        print("\n" + "="*80)
        print(f"RELATÓRIO DE EMBARGOS - {report['date']}")
        print("="*80)
        
        summary = report['summary']
        print(f"📊 RESUMO:")
        print(f"   • Total de downloads: {summary['total_downloads']}")
        print(f"   • Shapefiles válidos: {summary['valid_shapefiles']}")
        print(f"   • Arquivos alterados: {summary['changed_files']}")
        
        print(f"\n📋 DETALHES DOS DOWNLOADS:")
        for download in report['downloads']:
            status_shape = "✓" if download['is_shapefile'] else "✗"
            status_change = "🔄" if download['hash_changed'] else "➖"
            size_mb = download['file_size'] / (1024 * 1024)
            
            print(f"   {status_shape} {download['orgao']:<12} | {download['dataset']:<30} | {size_mb:.1f}MB {status_change}")
        
        print("="*80)
    
    async def run_full_process(self):
        """Executa o processo completo de validação, download e comparação."""
        try:
            self.logger.info("🚀 Iniciando processo completo de embargos...")
            
            # 1. Validar links
            self.logger.info("📡 Validando links...")
            link_results = await self.validate_links()
            valid_links = sum(1 for v in link_results.values() if v)
            total_links = len(link_results)
            self.logger.info(f"Links válidos: {valid_links}/{total_links}")
            
            # 2. Realizar downloads
            self.logger.info("📥 Iniciando downloads...")
            download_results = await self.download_all_embargos()
            
            # 3. Gerar relatório
            self.logger.info("📊 Gerando relatório...")
            report = self.generate_report()
            self.print_report(report)
            
            # 4. Exportar log
            self.logger_config.export_log(prefix="embargos_completo")
            
            self.logger.info("✅ Processo completo finalizado com sucesso!")
            
            return {
                'link_validation': link_results,
                'downloads': download_results,
                'report': report
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro no processo completo: {str(e)}")
            raise


async def main():
    """Função principal para executar o processamento de embargos."""
    processor = EmbargoProcessor()
    
    try:
        results = await processor.run_full_process()
        print("\n🎉 Processamento concluído com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro durante o processamento: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Executar o processo principal
    exit_code = asyncio.run(main())
    exit(exit_code)