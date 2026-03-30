1. Run build_vectorstore.py in Backend folder (once)

``` bash
python build_vectorstore.py
```

2. run the api

``` bash
python -m uvicorn api:app --reload
```

This will run the server at http://127.0.0.1:8000
Endpoint: POST /evaluate_claim



## create python virtual environment

```bash
python3.11 -m venv venv
```

## Activate virtual environment

```bash
source venv/bin/activate
```

## Install requirements.txt

```bash
uv pip install -r requirements.txt
```

## deactivate

```bash
deactivate
```

## Software tools

Protégé - ontology development environment
Langchain - LLM 
gemini-2.5-flash-lite model
Zotero - research papers management
MS Word - documentation

## OWN2VOWL ontology visualization with object classes

```zsh
(base) kaveesha@Kaveeshas-MacBook-Pro OWL2VOWL % java -jar target/OWL2VOWL-0.3.7-shaded.jar -file /Users/kaveesha/Documents/fyp/OWL/llm.owl  
```

```zsh
serve deploy/
```

find generated json file

```zsh
ls -lh *.json
```

Upload generated json file to webVOWL

## WebVOWL setup

Clone repo
https://github.com/VisualDataWeb/WebVOWL?tab=readme-ov-file

```zsh
npm install
```

```zsh
npm run-script release
```

if required, 
```zsh 
npm install serve -g
```

```zsh
serve deploy/
```
