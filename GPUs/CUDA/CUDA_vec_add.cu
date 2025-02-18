#include <stdio.h>
#include "cuda_runtime.h"



__global__ void add(int *d_a, int *d_b, int *d_c){

    int i = threadIdx.x;
    d_c[i] = d_a[i] + d_b[i];
}


int main(){

    cudaDeviceReset();
    int *d_a, *d_b, *d_c; //Device
    
    int *a, *b, *c; //Host

    int n = 2048;
    int size = n * sizeof(int);

    cudaError_t cudaStatus_1, cudaStatus_2, cudaStatus_3;

    a = (int*) malloc(size);
    b = (int*) malloc(size);
    c = (int*) malloc(size);

    cudaStatus_1 = cudaMalloc((void **) &d_a, size);
    cudaStatus_2 = cudaMalloc((void **) &d_b, size);
    cudaStatus_3 = cudaMalloc((void **) &d_c, size);

    if(cudaStatus_1 != cudaSuccess || cudaStatus_2 != cudaSuccess || cudaStatus_3 != cudaSuccess){
        printf("cudaMalloc Error!\n");
        exit(-1);
    }

    
    for(int i = 0; i < n; i++){
        a[i] = i;
        b[i] = i;
    }


    cudaMemcpy(d_a, a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, b, size, cudaMemcpyHostToDevice);

    add<<<1, n>>>(d_a, d_b, d_c);
    cudaDeviceSynchronize();

    cudaMemcpy(c, d_c, size, cudaMemcpyDeviceToHost);


    printf("Resultado da soma: \n");
    for(int i = 0; i < n; i++){
        printf("%d\n", c[i]);
    }

    return 0;


}