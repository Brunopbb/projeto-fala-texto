#!/bin/bash

HEAD_NODE="fala-texto@150.165.37.182"
WORKER_NODES=(
    "fala-texto@150.165.37.181"
    "fala-texto@150.165.37.162"
    "fala-texto@150.165.37.191"
    "fala-texto@150.165.37.184"
    "fala-texto-server2@150.165.37.51"
)

ray stop
ray start --head --port=6379 --dashboard-port=8265

echo "Head node iniciado em $HEAD_NODE"

sleep 5

HEAD_IP="150.165.37.182"

for NODE in "${WORKER_NODES[@]}"; do
    echo "Conectando $NODE ao cluster..."
    
    if [[ "$NODE" == "fala-texto-server2@150.165.37.51" ]]; then
        # Conectar na máquina que usa a porta SSH 59882
        ssh -p 59882 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -T "$NODE" << EOF
            ray stop
            ray start --address="$HEAD_IP:6379"
EOF
    else
        # Conectar nas máquinas que usam a porta SSH padrão (22)
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -T "$NODE" << EOF
            ray stop
            ray start --address="$HEAD_IP:6379"
EOF
    fi
    
    echo "$NODE conectado ao cluster."
done

echo "Cluster Ray iniciado com sucesso!"
