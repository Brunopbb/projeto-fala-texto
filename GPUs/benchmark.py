import ray
import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Inicializa o modelo PyTorch
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

# Função de treinamento
@ray.remote(num_cpus=4, num_gpus=0.5)
def train_worker(data):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    x = torch.rand(len(data), 10).to(device)
    y = torch.rand(len(data), 1).to(device)

    for epoch in range(500):  # Ajuste as épocas se necessário
        optimizer.zero_grad()
        outputs = model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

    return loss.item()

# Geração de dados
data = list(np.random.randint(0, 1000, size=10**7))  # 10 milhões de exemplos
chunk_size = 10**4
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Função para medir tempo e executar benchmark
def benchmark_ray(chunks, message):
    start_time = time.time()
    results = ray.get([train_worker.remote(chunk) for chunk in chunks])
    end_time = time.time()

    execution_time = end_time - start_time
    print(message)
    print(f"Tempo total de execução: {execution_time:.2f} segundos")
    return execution_time, results

# Inicializa o Ray
ray.init(address="auto")

# Fase 1: Executar apenas no nó head
print("Benchmark usando apenas o nó head:")
time_head, _ = benchmark_ray(chunks, "Resultado do benchmark com apenas o head.")

# Fase 2: Adicionar um worker e executar novamente
input("Adicione o worker e pressione Enter para continuar...")
print("\nBenchmark com head + worker:")
time_head_worker, _ = benchmark_ray(chunks, "Resultado do benchmark com head + worker.")

# Calcula métricas de desempenho
speedup = time_head / time_head_worker
efficiency = speedup / 4  # Dividido pelo número total de nós (head + 1 worker)

print("\nMétricas de desempenho:")
print(f"Aceleração (Speedup): {speedup:.2f}")
print(f"Eficiência de escalabilidade: {efficiency:.2%}")

# Encerra o Ray
ray.shutdown()
