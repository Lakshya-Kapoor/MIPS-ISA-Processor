#include <iostream>
using namespace std;

int main() {
    int num = 5;
    int reversed = 0;
    int original = num;
    while (num != 0) {
        reversed = reversed * 10 + num % 10;
        num /= 10;
    }
    if (original == reversed)
        cout << "It's a pallindrome" << endl;
    else
        cout << "It's not a pallindrome" << endl;
    return 0;
}