### Description
This project implements a semantic search pipeline for real-world XML data.

The data is first parsed and cleaned to handle inconsistencies and errors. Relevant information is extracted and preprocessed, followed by exploratory analysis of data distribution.

Different text chunking strategies were tested to determine an effective way of splitting documents for embedding. The processed text chunks are then stored in a vector database using ChromaDB to enable semantic search.

A simple interactive interface was built with Gradio to demonstrate the system, allowing users to input queries and retrieve the most relevant results.

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
Run the following command to create git hook for running pre-commit checks before each commit
```commandline
pre-commit install
```
