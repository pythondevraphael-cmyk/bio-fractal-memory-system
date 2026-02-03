# Bio-Fractal Memory System 🧠🌀

Uma aplicação Python de alta performance que mimetiza o crescimento de redes neurais biológicas e padrões fractais para persistência de conhecimento hierárquico.

## 🚀 Diferenciais Técnicos (Padrão Sênior)
- **Modelagem Adjacency List**: Implementação de autorreferência em SQL para ramificações infinitas.
- **Arquitetura Modular**: Separação clara entre persistência (`database.py`), lógica de negócio (`brain.py`) e orquestração (`main.py`).
- **Clean Code**: Tratamento de exceções, logs estruturados e total compatibilidade com encoding UTF-8/Windows.
- **BI Native**: Dashboard de estatísticas integrado para monitoramento de densidade da rede por nível.

## 🛠️ Tecnologias
- **Python 3.x**
- **SQLite3** (Persistência leve e portável)
- **Logging** (Rastreabilidade de processos)

## 📊 Estrutura de Dados
O sistema utiliza uma tabela única `synapses` onde cada "neurônio" possui um `parent_id`, permitindo que a inteligência do sistema se comporte como um organismo vivo em expansão.

## 📈 Como Executar
1. Clone o repositório.
2. Certifique-se de ter o Python instalado.
3. Execute: `python main.py`