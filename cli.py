import questionary
from questionary import Style
from src.config.bases_infos import (
    DATA_SOURCES_EMBARGOS, 
    DATA_SOURCES_DETER, 
    DATA_SOURCES_ALERTAS
)
from src.processors.Processor import Processor

# --- Estilo customizado para o questionary ---
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Marca de questão
    ('question', 'bold'),                # Texto da pergunta
    ('answer', 'fg:#f44336 bold'),       # Resposta selecionada
    ('pointer', 'fg:#673ab7 bold'),      # Ponteiro
    ('highlighted', 'fg:#673ab7 bold'),  # Item destacado
    ('selected', 'fg:#cc5454'),          # Item selecionado (checkbox)
    ('separator', 'fg:#cc5454'),         # Separador
    ('instruction', ''),                 # Instruções
    ('text', ''),                        # Texto normal
])

async def processar_base_especifica():
    """Menu para selecionar uma base específica de qualquer categoria"""
    print("\n" + "="*60)
    print("📊 SELECIONAR BASE ESPECÍFICA".center(60))
    print("="*60 + "\n")
    
    # Primeiro, escolhe a categoria
    categoria = await questionary.select(
        "Escolha a categoria:",
        choices=[
            questionary.Choice(title="🚫 Embargos", value="embargos"),
            questionary.Choice(title="⚠️  Desmatamento (Deter)", value="deter"),
            questionary.Choice(title="🔔 Alertas", value="alertas"),
            questionary.Choice(title="⬅️  Voltar", value="voltar")
        ],
        style=custom_style
    ).ask_async()
    
    if categoria == "voltar":
        return await main_menu()
    
    # Define qual dicionário usar baseado na categoria
    if categoria == "embargos":
        data_source = DATA_SOURCES_EMBARGOS
        process_name = "Embargos"
    elif categoria == "deter":
        data_source = DATA_SOURCES_DETER
        process_name = "Deter"
    else:  # alertas
        data_source = DATA_SOURCES_ALERTAS
        process_name = "Alertas"
    
    # Cria lista de órgãos disponíveis
    bases_disponiveis = []
    for orgao_key, orgao_info in data_source.items():
        orgao_name = orgao_info.name
        datasets_count = len(orgao_info.datasets)
        bases_disponiveis.append(
            questionary.Choice(
                title=f"🗂️  {orgao_name} ({datasets_count} dataset{'s' if datasets_count > 1 else ''})",
                value=orgao_key
            )
        )
    
    bases_disponiveis.append(questionary.Choice(title="⬅️  Voltar", value="voltar"))
    
    # Seleção do órgão
    orgao_selecionado = await questionary.select(
        "Escolha o órgão específico:",
        choices=bases_disponiveis,
        style=custom_style
    ).ask_async()
    
    if orgao_selecionado == "voltar":
        return await processar_base_especifica()
    
    # Obtém informações do órgão selecionado
    orgao_info = data_source[orgao_selecionado]
    
    print(f"\n{'='*60}")
    print(f"✅ Órgão selecionado: {orgao_info.name}")
    print(f"📦 Datasets: {len(orgao_info.datasets)}")
    for ds in orgao_info.datasets:
        print(f"   • {ds.slug}")
    print(f"{'='*60}\n")
    
    # Cria um dicionário com APENAS o órgão selecionado
    single_source = {orgao_selecionado: orgao_info}
    
    # Cria e retorna o Processor apenas com este órgão
    processor = Processor(
        process_name=process_name,
        data_sources=single_source,
        track_changes=True
    )
    
    return processor

async def main_menu():
    """Menu principal do sistema"""
    print("\n" + "="*60)
    print("🌿 DOWNLOAD DE BASES AMBIENTAIS".center(60))
    print("="*60 + "\n")
    
    opcao = await questionary.select(
        "Selecione uma opção:",
        choices=[
            "Embargos",
            "Deters",
            "Alertas",
            "Selecionar Base Específica",
            "Sair"
        ],
        style=custom_style
    ).ask_async()
    
    if opcao == "Sair":
        print("\nEncerrando o sistema...\n")
        exit(0)
        
    elif opcao == "Embargos":
        print("\n" + "="*60)
        print("🚫 PROCESSANDO EMBARGOS".center(60))
        print("="*60 + "\n")
        processor = Processor(process_name='Embargos', data_sources=DATA_SOURCES_EMBARGOS, track_changes=True)
        return processor
        
    elif opcao == "Deters":
        print("\n" + "="*60)
        print("⚠️  PROCESSANDO DETERS".center(60))
        print("="*60 + "\n")
        processor = Processor(process_name='Deters', data_sources=DATA_SOURCES_DETER, track_changes=False)
        return processor
        
    elif opcao == "Alertas":
        print("\n" + "="*60)
        print("🔔 PROCESSANDO ALERTAS".center(60))
        print("="*60 + "\n")
        processor = Processor(process_name='Alertas', data_sources=DATA_SOURCES_ALERTAS, track_changes=False)
        return processor
    
    elif opcao == "Selecionar Base Específica":
        return await processar_base_especifica()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_menu())