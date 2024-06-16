/*
16/6/24
220042162 Raiyan logic section part 2A

Find if its possible to visit all vertices
so, find if graph is connected

Given dataset:
Vertices: 8
Edges: [[a, b], [b, c], [d, c], [d, e], [f, c], [g, e], [a, d], [h, g], [i, h]]

*/

#include <bits/stdc++.h>
using namespace std;

bool isValid(const vector<bool>& visited, int vertices){
    for(int i= 0; i<vertices; i++){
        if(visited[i] == false) {
            return false;
        }

    }
    return true;
}

void bfs(int start , vector<bool> &visited,vector<vector<int>> adj_list) {
    queue<int> q;
    q.push(start);
    visited[start]= true;

    while (!q.empty()){
        int node = q.front();
        q.pop();
        for(int neighbor : adj_list[node]) {
            if(visited[neighbor]==false){
                q.push(neighbor);
                visited[neighbor]=true;
            }
        }

    }
}

int main() {
    int n;
    cout<<"Vertices: ";
    cin >>n;
    vector<bool> visited(9, false); // for 9 nodes in given dataset
    vector<vector<int>> adj_list(9);

    char a,b;
    cout<<"Edges  :  \n";
    for (int i= 0;i <adj_list.size() ; i++){
        cin >> a >> b;
        int x = a - 'a'; // convert letters to indexes
        int y = b - 'a';

        adj_list[x].push_back(y);
        adj_list[y].push_back(x);
    }

    bfs(0,visited, adj_list);
    if(isValid(visited,n)){
        cout<<"true\n";
    }
    else{
        cout<<"false\n";
    }

    return 0;

}

