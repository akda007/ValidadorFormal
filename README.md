# ⚙️ Validador Formal em Três Níveis

Projeto prático de Modelagem Computacional focado no reconhecimento de linguagens formais simulando um validador de logs e protocolos de rede. O projeto implementa três níveis da Hierarquia de Chomsky:
1. **Linguagem Regular (LR):** Autômato Finito Determinístico (DFA)
2. **Linguagem Livre de Contexto (LLC):** Autômato com Pilha (PDA)
3. **Linguagem Recursiva (R):** Máquina de Turing (MT)

## 📂 Estrutura do Repositório
* `src/`: Códigos-fonte dos validadores e scripts de automação.
* `testes/`: Baterias de testes em `.txt` com as cadeias aceitas e rejeitadas.
* `diagramas/`: Modelos formais desenhados via Graphviz.
* `relatorio/`: Documentação técnica completa em PDF.
* `app.py`: Interface Web desenvolvida em Streamlit.

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado. Instale as dependências executando:
```bash
pip install -r requirements.txt

```

### 1. Interface Web Interativa (Dashboard)

Para visualizar a execução passo a passo em uma interface rica, execute o Streamlit na raiz do projeto:

```bash
streamlit run app.py

```

Isso abrirá uma página no seu navegador onde você poderá testar logs personalizados, rodar toda a bateria de testes com um clique e visualizar a comparação de performance contra Regex.

### 2. Bateria de Testes Automatizada (Modo Terminal)

Se preferir rodar a validação completa via CLI (Linha de Comando), execute:

```bash
python src/testes.py

```

Este comando lê os arquivos dentro da pasta `testes/` e imprime a tabela comparativa (Esperado vs Obtido) e a quantidade exata de passos.

### 3. Validação Autônoma

Cada validador pode ser testado individualmente pelo terminal passando a cadeia como argumento:

```bash
python src/regular.py "LOGIN AUTH REQUEST LOGOUT"
python src/livre_contexto.py "BEGIN BEGIN END END"
python src/recursiva.py "OPEN COMMIT CLOSE"

```

---
