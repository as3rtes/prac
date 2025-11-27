#include <iostream>
using namespace std;

int main() {
    int size;

    cout << "Enter size: ";
    cin >> size;

    int* arr = new int[size];

    cout << "Enter elements:" << endl;
    for (int i = 0; i < size; i++) {
        cin >> arr[i];
    }

    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }

    cout << "Max: " << max << endl;


    return 0;
}