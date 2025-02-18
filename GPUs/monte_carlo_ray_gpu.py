import ray
import math
import time
import torch


GPU_CONFIG = {
    #"NVIDIA RTX 4500 Ada Generation": {"num_gpus": 1, "num_cpus": 16},
    "NVIDIA GeForce RTX 4080 SUPER": {"num_gpus": 1, "num_cpus": 10},
    #"NVIDIA GeForce RTX 4070 Ti SUPER": {"num_gpus": 1, "num_cpus": 8},
    "NVIDIA GeForce RTX 3070": {"num_gpus": 0.5, "num_cpus": 4},
    "NVIDIA GeForce RTX 3060": {"num_gpus": 0.5, "num_cpus": 6},
}

@ray.remote
class Progress:
    def __init__(self, total_num_samples: int):
        self.total_num_samples = total_num_samples
        self.num_samples_completed_per_task = {}

    def report_progress(self, task_id: int, num_samples_completed: int) -> None:
        self.num_samples_completed_per_task[task_id] = num_samples_completed

    def get_progress(self) -> float:
        return sum(self.num_samples_completed_per_task.values()) / self.total_num_samples


def get_gpu_type():
    if not torch.cuda.is_available():
        return "CPU"
    
    device = torch.cuda.current_device()
    gpu_name = torch.cuda.get_device_name(device)
    return gpu_name

@ray.remote
def sampling_task(num_samples: int, task_id, progress: ray.actor.ActorHandle) -> int:

    device = "cuda" if torch.cuda.is_available() else "cpu"

    x = torch.empty(num_samples, device=device).uniform_(-1, 1)
    y = torch.empty(num_samples, device=device).uniform_(-1, 1)

    num_inside = torch.sum(x**2 + y**2 <= 1).item()
    progress.report_progress.remote(task_id, num_samples)
    return num_inside


NUM_SAMPLES_PER_TASK = 100_000_000
TOTAL_TASKS = 10000
TOTAL_NUM_SAMPLES = NUM_SAMPLES_PER_TASK * TOTAL_TASKS

progress_actor = Progress.remote(TOTAL_NUM_SAMPLES)


results = []
for i in range(TOTAL_TASKS):
    gpu_name = get_gpu_type()
    gpu_config = GPU_CONFIG.get(gpu_name, {"num_gpus": 1, "num_cpus": 8})

    
    task = sampling_task.options(
        num_gpus=gpu_config["num_gpus"],
        num_cpus=gpu_config["num_cpus"]
    ).remote(NUM_SAMPLES_PER_TASK, i, progress_actor)

    results.append(task)


while True:
    progress = ray.get(progress_actor.get_progress.remote())
    print(f"Progresso: {int(progress * 100)}%")

    if progress >= 1:
        break

    time.sleep(1)


total_num_inside = sum(ray.get(results))
pi = (total_num_inside * 4) / TOTAL_NUM_SAMPLES
print(f"Estimativa de π: {pi}")


