# ✈️ SCRAPING-PROMILES

API FastAPI para scraping de preços de passagens aéreas (em reais e milhas) das principais companhias aéreas brasileiras.

## 📋 Descrição

Este projeto implementa uma API RESTful usando FastAPI para realizar scraping de informações de preços de passagens das seguintes companhias aéreas:

- **LATAM** (https://www.latamairlines.com/br/pt) - Programa LATAM Pass
- **GOL** (https://www.voegol.com.br/nh/) - Programa Smiles
- **AZUL** (https://www.voeazul.com.br/home/br/pt/home) - Programa TudoAzul

## 🎯 Objetivos

- Extrair preços em **reais (R$)**
- Extrair preços em **milhas/pontos**
- Implementar **dois métodos de scraping**:
  1. **Library-based**: Usando BeautifulSoup4 para parsing HTML
  2. **Regex-based**: Usando expressões regulares manuais

## 📁 Estrutura do Projeto

```
SCRAPING-PROMILES/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── models/
│   │   ├── __init__.py
│   │   └── flight.py        # Modelos Pydantic
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py  # Classe base abstrata
│   │   ├── latam_scraper.py # Scraper LATAM
│   │   ├── gol_scraper.py   # Scraper GOL
│   │   └── azul_scraper.py  # Scraper AZUL
│   └── routes/
│       ├── __init__.py
│       └── scrape.py        # Rotas da API
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Como Usar

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/JONTK123/SCRAPING-PROMILES.git
cd SCRAPING-PROMILES
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar a API

```bash
# Método 1: Usando uvicorn diretamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Método 2: Usando Python
python -m app.main
```

A API estará disponível em: http://localhost:8000

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔌 Endpoints

### 1. Root
```http
GET /
```
Retorna informações sobre a API.

### 2. Health Check
```http
GET /health
```
Verifica se a API está funcionando.

### 3. Listar Companhias Aéreas
```http
GET /scrape/airlines
```
Lista todas as companhias aéreas suportadas.

### 4. Scrape de uma Companhia
```http
POST /scrape/flight
Content-Type: application/json

{
  "airline": "latam",
  "method": "library",
  "origin": "GRU",
  "destination": "RIO",
  "departure_date": "2024-12-01"
}
```

**Parâmetros:**
- `airline`: "latam", "gol", ou "azul"
- `method`: "library" (BeautifulSoup) ou "regex" (expressões regulares)
- `origin`: (Opcional) Código do aeroporto de origem
- `destination`: (Opcional) Código do aeroporto de destino
- `departure_date`: (Opcional) Data de partida

**Resposta:**
```json
{
  "airline": "LATAM",
  "origin": "GRU",
  "destination": "RIO",
  "departure_date": "2024-12-01",
  "price_reais": 450.00,
  "price_miles": 15000,
  "scrape_method": "library",
  "scraped_at": "2024-10-27T11:16:51.986Z",
  "url": "https://www.latamairlines.com/br/pt",
  "status": "success",
  "error_message": null
}
```

### 5. Scrape de Todas as Companhias
```http
GET /scrape/all?method=library
```

Faz scraping de todas as companhias aéreas de uma vez.

**Parâmetros:**
- `method`: "library" ou "regex" (padrão: "library")

## 🛠️ Tecnologias Utilizadas

- **FastAPI** (0.104.1) - Framework web moderno e rápido
- **Uvicorn** (0.24.0) - Servidor ASGI
- **httpx** (0.25.1) - Cliente HTTP assíncrono
- **BeautifulSoup4** (4.12.2) - Parser HTML/XML
- **lxml** (4.9.3) - Parser XML/HTML rápido
- **Pydantic** (2.5.0) - Validação de dados

## 🔍 Métodos de Scraping

### 1. Library-based (BeautifulSoup)
Usa BeautifulSoup4 para fazer parsing do HTML e extrair informações de forma estruturada:
- Busca elementos HTML por classes e tags
- Navega na árvore DOM
- Extrai texto de elementos específicos

### 2. Regex-based (Expressões Regulares)
Usa padrões regex para extrair informações diretamente do HTML bruto:
- Padrões para preços em reais: `R$ 1.234,56`, `BRL 1234.56`
- Padrões para milhas: `15.000 milhas`, `pontos: 20000`
- Mais rápido mas menos robusto

## ⚠️ Considerações

- Este projeto é para fins educacionais e demonstração
- O scraping deve respeitar os termos de uso dos sites
- Os sites podem ter proteções contra scraping (CAPTCHA, rate limiting)
- A estrutura HTML dos sites pode mudar, quebrando os scrapers
- Recomenda-se usar APIs oficiais quando disponíveis

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Adicionar novos scrapers

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

JONTK123

---

**Nota**: Este projeto realiza scraping de dados públicos disponíveis nos sites das companhias aéreas. Certifique-se de respeitar os termos de uso de cada site ao usar esta API.
