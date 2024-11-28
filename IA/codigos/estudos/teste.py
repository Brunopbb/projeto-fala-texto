import json

import soundfile as sf
import librosa
import io
import os
import matplotlib.pyplot as plt

import numpy as np
import librosa.display

LOCAL_DATA_FILE = 'local_data.json'

if not os.path.exists(LOCAL_DATA_FILE):
    with open(LOCAL_DATA_FILE, 'w') as file:
        json.dump({'audio': [], 'transcription': []}, file)



data = {
    'audio': [],
    'transcription': []
}



samples1, sr1 = sf.read('/mnt/hd/audios_backup_test/VITRECTOMIA.wav')
samples2, sr2 = sf.read('/mnt/hd/audios_backup_test/TROPONINA.wav')

data['audio'].append({'array': samples1.tolist(), 'sampling_rate': sr1})
data['transcription'].append('VITRECTOMIA')

data['audio'].append({'array': samples2.tolist(), 'sampling_rate': sr2})
data['transcription'].append('TROPONINA')

with open(LOCAL_DATA_FILE, 'r+') as file:
    local_data = json.load(file)
    local_data['audio'].extend(data['audio'])
    local_data['transcription'].extend(data['transcription'])
    file.seek(0)
    json.dump(local_data, file)
    file.truncate()
    
audio, sr = librosa.load("/mnt/hd/audios_backup_test/VITRECTOMIA.wav", sr=16000)

plt.figure(figsize=(10, 4))
librosa.display.waveshow(audio, sr=sr)
plt.title("Forma de Onda")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.show()


espectrograma = np.abs(librosa.stft(audio))

# Exibir o espectrograma
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(espectrograma, ref=np.max), sr=sr, x_axis="time", y_axis="log")
plt.title("Espectrograma")
plt.colorbar(format="%+2.0f dB")
plt.show()