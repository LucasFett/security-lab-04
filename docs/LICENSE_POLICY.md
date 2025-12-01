# Política de Licenciamento de Software

## Objetivo
Definir critérios de aceitação para licenças de dependências de software.

## Licenças Permitidas ✅

### Permissivas (Aprovação Automática)
- **MIT License**
- **Apache License 2.0**
- **BSD License (2-Clause, 3-Clause)**
- **ISC License**
- **Python Software Foundation License**
- **Mozilla Public License 2.0**

### Características
- Uso comercial permitido
- Modificação permitida
- Distribuição permitida
- Sublicenciamento permitido

## Licenças que Requerem Revisão ⚠️

### Copyleft Fraco
- **LGPL (v2, v3)** - Requer revisão legal
- **MPL 1.1** - Requer análise de uso
- **EPL (Eclipse Public License)** - Requer revisão

### Processo de Revisão
1. Análise pelo time jurídico
2. Verificação de compatibilidade com licença do projeto
3. Documentação de uso e distribuição
4. Aprovação formal necessária

## Licenças Proibidas ❌

### Copyleft Forte
- **GPL (v2, v3)** - Proibido em projetos proprietários
- **AGPL (v3)** - Proibido (requer divulgação de código SaaS)

### Restrições Comerciais
- **Commons Clause**
- **Licenças "Non-Commercial"**

### Razões para Proibição
- Requerem divulgação de código fonte
- Incompatíveis com modelo de negócio
- Risco legal elevado

## Licenças Desconhecidas ❓

### Processo
1. Identificar licença através de SBOM
2. Pesquisar termos e condições
3. Classificar em uma das categorias acima
4. Atualizar lista de licenças conhecidas

## Auditoria e Compliance

### Frequência
- SBOM gerado em cada build
- Análise de licenças automática via CI/CD
- Revisão manual trimestral

### Responsabilidades
- **Desenvolvedores**: Verificar licenças antes de adicionar dependências
- **Segurança**: Manter lista de licenças aprovadas/proibidas
- **Jurídico**: Revisar casos especiais

### Ferramentas
- Syft - Geração de SBOM
- pip-licenses - Análise de licenças Python
- Custom scripts - Verificação de políticas

## Exceções

### Processo de Exceção
1. Justificativa técnica e de negócio
2. Análise de alternativas
3. Revisão jurídica
4. Aprovação de stakeholders
5. Documentação e monitoramento

### Critérios
- Dependência crítica sem alternativa
- Uso isolado (não distribucional)
- Benefício supera risco

## Atualizações da Política

Esta política deve ser revisada:
- Anualmente
- Quando mudanças regulatórias ocorrerem
- Quando novo modelo de negócio for adotado

**Última atualização:** 30 de Novembro de 2025
