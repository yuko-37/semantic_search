## 1. Install Ollama
Download and install Ollama by following the official documentation:<br/>
https://docs.ollama.com/<br/>
After installation, verify it is available in your terminal:<br/>
```bash 
ollama --version
```

## 2. Create conda environment
Create the project’s conda environment using the provided `environment.yml` file:<br/>
```bash
conda env create -f environment.yml
```
Activate the environment:<br/>
```bash
conda activate semantic_search
```

## 3. Start Ollama
Some notebooks (e.g., those using embedding models) require Ollama to be running.<br/>
Start the Ollama server before executing those notebooks:<br>
```bash 
ollama serve
```