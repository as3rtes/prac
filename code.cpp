#include <iostream>
using namespace std;

int main() {
    int arr[] = {33,45,23,944,1, 82};
    int size = 6;

    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    cout << "Max: " << max << endl;
    return 0;
}