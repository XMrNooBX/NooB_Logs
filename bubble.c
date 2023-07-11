#include <stdio.h>
#include <stdlib.h>
void swap(int arr[], int index1, int index2, int length){
    if(index2<length){int temp = arr[index1];
    arr[index1] = arr[index2];
    arr[index2] = temp;}
}
void bubble(int arr[],int length){
    for(int i=0; i<=length-1; i++){
        for(int k=0; k<=length-1; k++){
            
            if(arr[k]>=arr[k+1]){swap(arr, k, k+1,length);}
        
        }
    }
}
int main(){
    int arr[] = {5, 10, 102, 8, 6, 5, 0, 67, -5, -2};
    int length = sizeof(arr)/sizeof(arr[0]);
    bubble(arr,length);
   for(int j=0; j<=length-1; j++){
        printf("%i\n",arr[j]);
    }
return 0;}
