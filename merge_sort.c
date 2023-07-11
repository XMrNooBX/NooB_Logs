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
    int arr_1[] = {5, 10, 102, 8, 6, 5, 0, 67, -5, -2};
    int arr_2[] = {2, 8, -9, 7, 3, 0, 55, 8};
    int length_1 = sizeof(arr_1)/4, length_2 = sizeof(arr_2)/4;

bubble(arr_1,length_1);
bubble(arr_2,length_2);

int arr_3[length_1+length_2];

for(int i=0; i<=length_1-1;i++){arr_3[i]=arr_1[i];}
for (int i = 0, j = length_1;j < length_1+length_2 && i < length_2; i++, j++){arr_3[j] = arr_2[i];}

bubble(arr_3,length_1+length_2);

for(int i=0; i<=length_1+length_2-1; i++){printf("%i\n",arr_3[i]);}
return 0;}