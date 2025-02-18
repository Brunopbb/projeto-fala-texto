#include "cuda_runtime.h"
#include <stdio.h>



__global__ void vec_constMult(int N, float *d_vec, float num){

    int i = threadIdx.x;
    while(i < N){

        d_vec[i] = d_vec[i] * num;
        i += blockDim.x;

    }
    
}


int main(){

    cudaDeviceReset();
    float *vec;
    int n = 2048;
    int size = n * sizeof(int);
    float *d_vec;
    float num = 2;
    
    cudaError_t cudaStatus;

    //Aloca memória na CPU
    vec = (float*) malloc(size);

    //aloca memória da GPU
    cudaStatus = cudaMalloc((void **) &d_vec, size);

    if(cudaStatus != cudaSuccess){
        printf("Error!\n");
        exit(-1);
    }

    for(int i = 0; i < n; i++){
        vec[i] = i;
    }

    

    //Copia os dados da CPU para a memória global da GPU
    cudaMemcpy(d_vec, vec, size, cudaMemcpyHostToDevice);

    //Host chama o kernel
    vec_constMult<<<1, 1024>>>(n, d_vec, num);
    cudaDeviceSynchronize();

    //Copia da memoria da GPU para a CPU
    cudaMemcpy(vec, d_vec, size, cudaMemcpyDeviceToHost);

    
    for(int i = 0; i < n; i++){
        printf("%.2f ", vec[i]);
    }


    return 0;
}