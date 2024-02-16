# include <bits/stdc++.h>
using namespace std;

int main(){
    vector<vector<int>> arr = {{1,2,3,4},{5,6,7,8},{9,10,11,12}, {13,14,15,16}};
    for (int i = 0; i < arr.size(); i++)
        for (int j = i+1; j < arr.size(); j++)
            swap(arr[i][j], arr[j][i]);
    for (auto it : arr){
        for (auto x : it)
            cout << x << " ";
        cout << endl;
    }
}