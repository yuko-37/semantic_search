### Description
Project that processes xml files and push them in vector storage to enable semantic search.

### 1. Install Ollama
Download and install Ollama by following the official documentation:<br/>
https://docs.ollama.com/<br/>
After installation, verify it is available in your terminal:<br/>
```bash 
ollama --version
```

### 2. Create conda environment
Create the project’s conda environment using the provided `environment.yml` file:<br/>
```bash
conda env create -f environment.yml
```
use the command below to update environment
```bash
conda env update --name semantic_search --file=environment.yml --prune
```
Activate the environment:<br/>
```bash
conda activate semantic_search
```
Start jupyter lab:<br/>
```bash
jupyter lab
```

### 3. Start Ollama
Some notebooks (e.g., those using embedding models) require Ollama to be running.<br/>
Start the Ollama server before executing those notebooks:<br>
```bash 
ollama serve
```

### 4. For Development
Use conda to install dev tool on your base environment
```bash
conda install -c conda-forge ruff black pre-commit
```
or pip install
```commandline
pip install ruff black pre-commit
```
Run the following command to create git hook for
```commandline
pre-commit install
```
