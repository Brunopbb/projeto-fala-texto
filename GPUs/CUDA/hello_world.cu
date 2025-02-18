#include "cuda_runtime.h"
#include <stdio.h>

//Kernel

__global__ void myKernel(){

    printf("Hello World da GPU\n");

}


//CPU
int main(){

    myKernel <<<3, 5>>> ();
    printf("Hello World\n");
    cudaDeviceSynchronize();

    

    return 0;
}