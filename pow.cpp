#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, x, y = 1;
    cin >> x >> n;
    while (n) {
        if (n % 2 == 1) y = y * x;
        x = x * x;
        n = n / 2;
    }
    cout << y << endl;
}