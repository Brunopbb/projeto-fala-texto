import os
import torch
from nemo.collections.asr.models import EncDecCTCModel
from omegaconf import OmegaConf

# 📌 Configurações
MODEL_NAME = "stt_en_conformer_ctc_large"
CHECKPOINT_PATH = f"nemo_checkpoints/{MODEL_NAME}.nemo"
OUTPUT_PATH = "commonvoice_json"

# 📌 Carregar modelo pré-treinado
print("🔹 Carregando modelo...")
asr_model = EncDecCTCModel.restore_from(CHECKPOINT_PATH)

# 📌 Configuração do treinamento
config = OmegaConf.create({
    "model": {
        "train_ds": {
            "manifest_filepath": os.path.join(OUTPUT_PATH, "train.json"),
            "batch_size": 32,
            "shuffle": True,
            "num_workers": 8,
            "sample_rate": 16000  # 🔹 A taxa de amostragem dos áudios
        },
        "validation_ds": {
            "manifest_filepath": os.path.join(OUTPUT_PATH, "validation.json"),
            "batch_size": 32,
            "shuffle": False,
            "num_workers": 8,
            "sample_rate": 16000  # 🔹 A taxa de amostragem dos áudios
        },
        "test_ds": {
            "manifest_filepath": os.path.join(OUTPUT_PATH, "test.json"),
            "batch_size": 32,
            "shuffle": False,
            "num_workers": 8,
            "sample_rate": 16000  # 🔹 A taxa de amostragem dos áudios
        }
    },
    "trainer": {
        "gpus": torch.cuda.device_count(),
        "max_epochs": 50,
        "accelerator": "gpu",
        "precision": 16
    }
})

# 📌 Aplicar configuração e iniciar treino
print("🔹 Iniciando treinamento...")
asr_model.setup_training_data(train_data_config=config.model.train_ds)
asr_model.setup_validation_data(val_data_config=config.model.validation_ds)
asr_model.setup_test_data(test_data_config=config.model.test_ds)
asr_model.train()
print("✅ Treinamento finalizado!")
