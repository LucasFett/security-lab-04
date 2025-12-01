#!/usr/bin/env python3
"""
Compara dois SBOMs e identifica mudanças em dependências
"""

import json
import sys
from datetime import datetime

def load_sbom(filepath):
    """Carrega SBOM em formato CycloneDX"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_components(sbom):
    """Extrai componentes do SBOM (nome e versão)"""
    components = {}
    if 'components' in sbom:
        for comp in sbom['components']:
            name = comp['name']
            version = comp.get('version', 'unknown')
            components[name] = version
    return components

def compare(old_sbom, new_sbom):
    """Compara dois SBOMs"""
    old_comp = extract_components(old_sbom)
    new_comp = extract_components(new_sbom)
    
    added = {k: v for k, v in new_comp.items() if k not in old_comp}
    removed = {k: v for k, v in old_comp.items() if k not in new_comp}
    updated = {k: (old_comp[k], new_comp[k]) 
               for k in old_comp.keys() & new_comp.keys() 
               if old_comp[k] != new_comp[k]}
    
    return added, removed, updated

def print_report(added, removed, updated):
    """Imprime relatório de mudanças"""
    print("\n" + "="*70)
    print("📊 RELATÓRIO DE COMPARAÇÃO DE SBOMs")
    print("="*70 + "\n")
    
    if added:
        print(f"➕ DEPENDÊNCIAS ADICIONADAS ({len(added)}):")
        print("-" * 70)
        for name, version in sorted(added.items()):
            print(f"  + {name} @ {version}")
        print()
    
    if removed:
        print(f"➖ DEPENDÊNCIAS REMOVIDAS ({len(removed)}):")
        print("-" * 70)
        for name, version in sorted(removed.items()):
            print(f"  - {name} @ {version}")
        print()
    
    if updated:
        print(f"🔄 DEPENDÊNCIAS ATUALIZADAS ({len(updated)}):")
        print("-" * 70)
        for name, (old_ver, new_ver) in sorted(updated.items()):
            print(f"  ↻ {name}: {old_ver} → {new_ver}")
        print()
    
    if not (added or removed or updated):
        print("✅ Nenhuma mudança detectada entre os SBOMs\n")
    
    print(f"📅 Comparação realizada em: {datetime.now().isoformat()}\n")

def main():
    if len(sys.argv) < 3:
        print("Uso: python compare-sboms.py <old-sbom.json> <new-sbom.json>")
        sys.exit(1)
    
    old_file = sys.argv[1]
    new_file = sys.argv[2]
    
    try:
        old_sbom = load_sbom(old_file)
        new_sbom = load_sbom(new_file)
        
        added, removed, updated = compare(old_sbom, new_sbom)
        print_report(added, removed, updated)
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
