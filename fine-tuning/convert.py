import os
import json
import shutil
import librosa
from datasets import load_dataset
from tqdm import tqdm

# 📌 Configurações
DATASET_NAME = "mozilla-foundation/common_voice_17_0"
LANGUAGE = "pt"
OUTPUT_PATH = "commonvoice_json"
AUDIO_DIR = "audio_files"  # Diretório para armazenar os áudios

# 📌 Baixar o dataset do Hugging Face
print("🔹 Baixando dataset do Hugging Face...")
dataset = load_dataset(DATASET_NAME, LANGUAGE)

# 📌 Criar diretórios para salvar os arquivos JSON e áudios
os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# 📌 Função para copiar os áudios para o diretório local
def copy_audio(audio_path, local_path):
    if not os.path.exists(local_path):
        shutil.copy(audio_path, local_path)
        print(f"Áudio {os.path.basename(local_path)} copiado com sucesso.")
    else:
        print(f"Áudio {os.path.basename(local_path)} já existe.")

# 📌 Converter para formato NeMo e garantir que os áudios sejam copiados
def convert_to_nemo_json(split, dataset):
    json_path = os.path.join(OUTPUT_PATH, f"{split}.jsonl")
    with open(json_path, "w", encoding="utf-8") as f:
        for example in tqdm(dataset[split]):
            if example["audio"]["array"] is None:
                continue
            
            # Caminho do áudio local
            audio_path = example["audio"]["path"]
            local_audio_path = os.path.join(AUDIO_DIR, os.path.basename(audio_path))

            # Copiar o áudio para a pasta local
            copy_audio(audio_path, local_audio_path)

            # Obter duração do áudio
            duration = librosa.get_duration(path=local_audio_path)

            # Adicionar dados ao JSONL
            json_line = json.dumps({
                "audio_filepath": local_audio_path,
                "text": example["sentence"],
                "duration": duration
            }, ensure_ascii=False)
            f.write(json_line + "\n")
    print(f"✅ Arquivo salvo: {json_path}")

# Gerar arquivos de treino, validação e teste
convert_to_nemo_json("train", dataset)
convert_to_nemo_json("validation", dataset)
convert_to_nemo_json("test", dataset)
