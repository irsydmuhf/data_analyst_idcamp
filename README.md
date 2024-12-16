# Dicoding Collection Dashboard ✨

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
Jika belum menginstall pipreqs, install dengan cara:
pip install pipreqs
Jika sudah menginstall pipreqs, langsung ketik:
pipreqs .
notes: "." di atas berarti direktori saat ini
Jika kamu tidak sedang berada di dalam direktori, ketik:
pipreqs /path/ke/projek
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```