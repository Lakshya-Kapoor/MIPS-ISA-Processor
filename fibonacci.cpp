#include <bits/stdc++.h>
using namespace std;
int main() {
    int a = 0, b = 1, c;
    int n = 5;
    while (--n) {
        c = a + b;
        a = b;
        b = c;
    }
    cout << c << endl;
    return 0;
}