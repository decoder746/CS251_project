#include <iostream>
using namespace std;

int intc(char x){
	if(x=='.'){return 0;}
	else{int y=x-'0';
	return y;}
}

int main(){
	int x;
	cin>>x;
	for(int k=0;k<x;k++){
		string s;
		cin>>s;
		int n=s.size();
		int a[n];
		int b[n];
		bool z=0;
		for(int i=0; i<n; i++){
			a[i]=intc(s[i]);
			if(a[i]>0){z=1;}
			b[i]=0;
			//cout<<a[i];
		}
		if(z==0){cout<<"safe"<<'\n';continue;}


		for(int i=0;i<n;i++){
			if(a[i]!=0){
				bool un=0;
				for(int j=min(0,i-a[i]);j<max(n+1,i+a[i]+1);j++){
					if (b[j]>0){
						cout<<"unsafe"<<'\n';
						un=1;
						break;
					}
					else{b[j]=1;
					}

				}
				if(un==1){
					break;
				}
				else{
					cout<<"safe"<<'\n';
				}
			}
		}

	}
}