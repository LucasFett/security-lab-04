#!/usr/bin/env python3
"""
Script para analisar licenças e verificar conformidade
"""

import json
import sys
from collections import Counter

# Licenças permitidas (exemplo de policy)
ALLOWED_LICENSES = {
    'MIT', 'MIT License',
    'Apache Software License', 'Apache 2.0', 'Apache-2.0',
    'BSD License', 'BSD', '3-Clause BSD',
    'ISC License', 'ISC',
    'Python Software Foundation License',
    'Mozilla Public License 2.0 (MPL 2.0)'
}

# Licenças proibidas (copyleft forte)
FORBIDDEN_LICENSES = {
    'GNU General Public License v2 (GPLv2)',
    'GNU General Public License v3 (GPLv3)',
    'GNU Affero General Public License v3 (AGPLv3)',
    'GPL', 'GPLv2', 'GPLv3', 'AGPL'
}

# Licenças que requerem revisão
REVIEW_REQUIRED = {
    'GNU Lesser General Public License v2 (LGPLv2)',
    'GNU Lesser General Public License v3 (LGPLv3)',
    'LGPL', 'LGPLv2', 'LGPLv3',
    'Creative Commons'
}

def load_sbom(filepath):
    """Carrega SBOM em formato CycloneDX"""
    with open(filepath, 'r') as f:
        return json.load(f)

def analyze_licenses(sbom):
    """Analisa licenças no SBOM e extrai informações"""
    licenses = []
    
    # Verifica se o SBOM está no formato CycloneDX e tem componentes
    if 'components' in sbom:
        for comp in sbom['components']:
            lic_name = 'Unknown'
            
            # Tenta extrair a licença do campo 'licenses'
            if 'licenses' in comp and comp['licenses']:
                # Assume a primeira licença encontrada
                lic = comp['licenses'][0]
                if 'license' in lic and 'name' in lic['license']:
                    lic_name = lic['license']['name']
                elif 'expression' in lic:
                    lic_name = lic['expression']
            
            licenses.append({
                'component': comp['name'],
                'version': comp.get('version', 'N/A'),
                'license': lic_name
            })
            
    return licenses

def check_compliance(licenses):
    """Verifica conformidade com políticas de licenciamento"""
    issues = {
        'forbidden': [],
        'review_required': [],
        'allowed': [],
        'unknown': []
    }
    
    for lic_info in licenses:
        lic = lic_info['license']
        
        # Normaliza a licença para comparação
        lic_norm = lic.split('(')[0].strip()
        
        if lic_norm in FORBIDDEN_LICENSES or lic in FORBIDDEN_LICENSES:
            issues['forbidden'].append(lic_info)
        elif lic_norm in REVIEW_REQUIRED or lic in REVIEW_REQUIRED:
            issues['review_required'].append(lic_info)
        elif lic_norm in ALLOWED_LICENSES or lic in ALLOWED_LICENSES:
            issues['allowed'].append(lic_info)
        else:
            issues['unknown'].append(lic_info)
    
    return issues

def generate_report(issues):
    """Gera relatório de compliance"""
    print("\n" + "="*60)
    print("📄 RELATÓRIO DE ANÁLISE DE LICENÇAS")
    print("="*60 + "\n")
    
    # Estatísticas
    total = sum(len(v) for v in issues.values())
    print(f"Total de componentes analisados: {total}\n")
    
    # Licenças proibidas
    if issues['forbidden']:
        print("❌ LICENÇAS PROIBIDAS (CRITICAL):")
        print("-" * 60)
        for item in issues['forbidden']:
            print(f"  - {item['component']} {item['version']}: {item['license']}")
        print()
    
    # Licenças que requerem revisão
    if issues['review_required']:
        print("⚠️  LICENÇAS QUE REQUEREM REVISÃO:")
        print("-" * 60)
        for item in issues['review_required']:
            print(f"  - {item['component']} {item['version']}: {item['license']}")
        print()
    
    # Licenças desconhecidas
    if issues['unknown']:
        print("❓ LICENÇAS DESCONHECIDAS:")
        print("-" * 60)
        for item in issues['unknown']:
            print(f"  - {item['component']} {item['version']}: {item['license']}")
        print()
    
    # Resumo
    print("✅ RESUMO:")
    print("-" * 60)
    print(f"  Permitidas: {len(issues['allowed'])}")
    print(f"  Requerem revisão: {len(issues['review_required'])}")
    print(f"  Desconhecidas: {len(issues['unknown'])}")
    print(f"  Proibidas: {len(issues['forbidden'])}")
    print()
    
    # Exit code
    if issues['forbidden']:
        print("❌ FALHA: Licenças proibidas detectadas!")
        return 1
    elif issues['review_required']:
        print("⚠️  ATENÇÃO: Licenças requerem revisão legal")
        return 0
    else:
        print("✅ SUCESSO: Todas as licenças estão em conformidade")
        return 0

def main():
    if len(sys.argv) < 2:
        print("Uso: python analyze-licenses.py <sbom.json>")
        sys.exit(1)
    
    sbom_file = sys.argv[1]
    
    try:
        sbom = load_sbom(sbom_file)
        licenses = analyze_licenses(sbom)
        issues = check_compliance(licenses)
        exit_code = generate_report(issues)
        sys.exit(exit_code)
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
