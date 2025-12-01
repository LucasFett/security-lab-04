# RELATÓRIO DE ATIVIDADE - SBOM Generation e Compliance

**Autor:** Manus AI
**Data:** 30 de Novembro de 2025

## 1. Introdução

Este relatório documenta a execução da Atividade 04, focada na geração automatizada de Software Bill of Materials (SBOM), análise de dependências, validação de licenças e garantia de conformidade com políticas de segurança. O SBOM é um inventário formal e estruturado de componentes de software e suas dependências, essencial para a gestão de riscos na cadeia de suprimentos de software (Software Supply Chain Security) [1].

## 2. Geração de SBOM

A geração do SBOM foi realizada utilizando a ferramenta **Syft**, que analisou o projeto Python baseado no arquivo `requirements.txt` e o código-fonte.

### 2.1 Componentes Identificados

O projeto de exemplo, incluindo as dependências diretas e transitivas, resultou na identificação de **aproximadamente 22 pacotes** principais (conforme output do Syft) e suas dependências aninhadas.

### 2.2 Formatos de SBOM

Foram gerados SBOMs nos dois formatos mais utilizados na indústria:
*   **SPDX (Software Package Data Exchange):** Formato padrão ISO/IEC 5962:2021, gerado em `local-sbom-spdx.json`.
*   **CycloneDX:** Formato leve e focado em segurança, gerado em `local-sbom-cyclonedx.json`.

## 3. Análise de Vulnerabilidades

A análise de vulnerabilidades foi realizada utilizando a ferramenta **Grype**, que consumiu o SBOM gerado em formato SPDX.

### 3.1 Resumo de Vulnerabilidades

A varredura identificou um total de **35 vulnerabilidades** nas dependências do projeto. O resumo por severidade é apresentado na tabela abaixo:

| Severidade | Quantidade | CVEs de Exemplo |
|------------|------------|-----------------|
| Critical | 3 | GHSA-pv4p-cwwg-4rph, GHSA-r3xc-prgr-mg9p, GHSA-frmv-pr5f-9mcr |
| High | 13 | GHSA-jh3w-4vvf-mjgr, GHSA-f6f8-9mx6-9mx2, GHSA-qmf9-6jqf-j8fq |
| Medium | 18 | GHSA-5hgc-2vfp-mqvc, GHSA-vm8q-m57g-pff3, GHSA-p3fp-8748-vqfq |
| Low | 1 | - |

### 3.2 Componentes Vulneráveis

Os principais componentes vulneráveis identificados foram:
1.  **django @ 4.2.0** - **Critical** (GHSA-pv4p-cwwg-4rph) - Múltiplas vulnerabilidades de alta severidade.
2.  **cryptography @ 41.0.7** - **High** (GHSA-3ww4-gg4f-jr7f) - Vulnerabilidade de alta severidade.
3.  **requests @ 2.31.0** - **Medium** (GHSA-9hjg-9r4m-mvj7) - Vulnerabilidade de severidade média.

### 3.3 Recomendações de Atualização

A principal recomendação é a atualização imediata dos pacotes com vulnerabilidades críticas e altas.
- **django**: versão atual `4.2.0` → versão segura **`4.2.26`** (ou superior).
- **cryptography**: versão atual `41.0.7` → versão segura **`43.0.1`** (ou superior).
- **requests**: versão atual `2.31.0` → versão segura **`2.32.5`** (ou superior).

## 4. Automação Implementada

A automação foi projetada para ser executada em um ambiente de Integração Contínua/Entrega Contínua (CI/CD), utilizando GitHub Actions.

### 4.1 GitHub Actions Workflows
- [x] **sbom-generation.yml**: Workflow principal que orquestra a geração de SBOM, análise de licenças, scan de vulnerabilidades e geração da árvore de dependências.
- [ ] **license-compliance.yml**: (Não implementado no ambiente local, mas essencial para a prática) Workflow para verificar o compliance de licenças em Pull Requests, bloqueando merges em caso de violação de política.

### 4.2 Scripts Desenvolvidos
- [x] **analyze-licenses.py**: Script Python customizado para verificar a conformidade das licenças do SBOM com a política definida em `docs/LICENSE_POLICY.md`.
- [x] **compare-sboms.py**: Script Python para comparar dois SBOMs (e.g., antes e depois de uma atualização) e identificar dependências adicionadas, removidas ou atualizadas.

## 5. Política de Licenciamento

A política de licenciamento foi definida no arquivo `docs/LICENSE_POLICY.md`.

### 5.1 Critérios Definidos
- **Licenças Permitidas**: MIT, Apache 2.0, BSD, ISC, Python Software Foundation License, Mozilla Public License 2.0.
- **Licenças que Requerem Revisão**: LGPL (v2, v3), MPL 1.1, EPL.
- **Licenças Proibidas**: GPL (v2, v3), AGPL (v3), Commons Clause, Licenças "Non-Commercial".
- **Processo de Exceção**: Justificativa técnica, análise de alternativas, revisão jurídica e aprovação de stakeholders.

### 5.2 Enforcement
A verificação de compliance é realizada automaticamente via CI/CD (e pelo script `analyze-licenses.py` localmente), garantindo que licenças proibidas sejam detectadas e que o processo de desenvolvimento seja interrompido ou notificado.

## 6. Integração com Segurança

A integração com segurança é realizada através de um pipeline automatizado que transforma o código em um artefato seguro e auditável:

**Code Push → SBOM Generation → License Check → Vulnerability Scan → Compliance Report**

### 6.2 Benefícios
- **Visibilidade completa** de todos os componentes de software.
- **Detecção precoce** de licenças problemáticas e vulnerabilidades.
- **Rastreabilidade** de componentes para auditoria e resposta a incidentes.

## 7. Casos de Uso

### 7.1 Auditoria de Segurança
O SBOM fornece um inventário completo, facilitando a resposta a vulnerabilidades e permitindo identificar rapidamente quais componentes estão afetados por uma nova falha de segurança (e.g., uma nova CVE).

### 7.2 Compliance Regulatório
Documentação essencial para atender a requisitos regulatórios, como a Executive Order 14028 nos EUA, que exige SBOMs para software vendido ao governo federal [2].

## 8. Comparação de Ferramentas

### 8.1 Syft vs CycloneDX Python

| Aspecto | Syft | CycloneDX Python |
|---------|------|------------------|
| Cobertura | Multi-linguagem (código, imagens, arquivos) | Python apenas (baseado em `requirements.txt`) |
| Formatos | SPDX, CycloneDX, etc | CycloneDX |
| Detalhamento | Alto | Muito alto (focado no ecossistema Python) |
| Uso | Ideal para análise de repositórios e imagens de contêiner | Ideal para geração de SBOMs leves e precisos de projetos Python |

## 9. Lições Aprendidas

### 9.1 Principais Insights
1.  **A Importância da Automação:** A geração manual de SBOMs é inviável. A integração em CI/CD é crucial para manter o inventário atualizado.
2.  **Vulnerabilidades em Dependências:** Mesmo em um projeto simples, dependências de terceiros (como `django` e `cryptography`) introduzem vulnerabilidades que exigem monitoramento e atualização contínuos.
3.  **Desafio das Licenças:** A identificação e o mapeamento de licenças podem ser complexos, exigindo ferramentas robustas como `pip-licenses` e scripts customizados para fazer o *enforcement* da política.

### 9.2 Desafios Encontrados
- A necessidade de permissões elevadas (`sudo`) para instalar ferramentas como Syft e Grype no ambiente de sandbox.
- A complexidade na extração de informações de licença de SBOMs gerados por diferentes ferramentas, reforçando a necessidade de normalização.

### 9.3 Importância do SBOM
O SBOM é a base da segurança da cadeia de suprimentos de software. Ele transforma um "black box" de dependências em um inventário transparente, permitindo que as equipes de segurança e jurídica tomem decisões informadas sobre riscos e conformidade.

## 10. Melhorias Futuras

- [ ] Integrar o SBOM com um sistema de gestão de vulnerabilidades (e.g., DefectDojo) para rastreamento contínuo.
- [ ] Implementar assinatura digital de SBOMs para garantir a integridade e autenticidade.
- [ ] Criar um dashboard de compliance para visualização rápida do status de segurança e licenças.

## 11. Conclusão

A geração de SBOM e a verificação de compliance são práticas indispensáveis na engenharia de software moderna. A atividade demonstrou que, ao automatizar a criação de SBOMs em formatos padronizados (SPDX e CycloneDX), é possível realizar análises críticas de vulnerabilidades (Grype) e conformidade de licenças (scripts customizados) de forma eficiente. O SBOM não é apenas um requisito regulatório crescente, mas uma ferramenta fundamental para a transparência, gestão de riscos e fortalecimento da segurança da cadeia de suprimentos de software.

## 12. Evidências

Os seguintes arquivos foram gerados e servem como evidência da execução da atividade:

### Arquivos Gerados
- `local-sbom-spdx.json` (SBOM em formato SPDX)
- `local-sbom-cyclonedx.json` (SBOM em formato CycloneDX)
- `licenses.md` (Relatório de licenças gerado por `pip-licenses`)
- `grype-sbom-results.json` (Resultados do scan de vulnerabilidades)
- `grype-sbom-results.txt` (Resultados do scan de vulnerabilidades em formato de tabela)
- `dependency-tree.txt` (Árvore de dependências)
- `RELATORIO.md` (Este documento)
- `docs/LICENSE_POLICY.md` (Política de Licenciamento)
- `scripts/analyze-licenses.py` (Script de análise de licenças)
- `scripts/compare-sboms.py` (Script de comparação de SBOMs)
- `.github/workflows/sbom-generation.yml` (Workflow de automação)

### Screenshots (Em um ambiente real de CI/CD)
Em um ambiente real de GitHub, seriam incluídos screenshots da execução do workflow, do SBOM em formato de tabela e do relatório de licenças para comprovar a automação.

## 13. Referências

[1] NTIA SBOM: https://www.ntia.gov/SBOM
[2] Executive Order 14028: https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/
[3] Syft: https://github.com/anchore/syft
[4] Grype: https://github.com/anchore/grype
