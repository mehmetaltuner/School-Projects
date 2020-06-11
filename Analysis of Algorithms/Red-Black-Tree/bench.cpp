#include <set>
#include <cstdlib>
#include <iostream>
#include <ctime>
#include "rbt.h"

using namespace std;

const int tc = 1e6;

int main(){
	ios_base::sync_with_stdio(0);

	srand(time(nullptr));
	multiset <int> st;

	clock_t begin = clock();
	for(int i=0; i<tc; i++){
		st.insert(i);
	}
	clock_t end = clock();
	cout << "CPP SET INSERT TIME OVER " << tc << " CASES: " << endl << fixed << double(end-begin) / CLOCKS_PER_SEC << endl;

	rb <int> rbt;

	begin = clock();
	for(int i=0; i<tc; i++){
		rbt.insert(i);
	}
	end = clock();
	cout << "RBT INSERT TIME OVER " << tc << " CASES: " << endl << fixed << double(end-begin) / CLOCKS_PER_SEC << endl;

	begin = clock();
	for(int i=0; i<tc; i++){
		st.find(i);
	}
	end = clock();
	cout << "CPP SET FIND TIME OVER " << tc << " CASES: " << endl << fixed << double(end-begin) / CLOCKS_PER_SEC << endl;

	begin = clock();
	for(int i=0; i<tc; i++){
		rbt.find(i);
	}
	end = clock();
	cout << "RBT FIND TIME OVER " << tc << " CASES: " << endl << fixed << double(end-begin) / CLOCKS_PER_SEC << endl;

	begin = clock();
	for(int i=0; i<tc; i++){
		st.erase(i);
	}
	end = clock();
	cout << "CPP SET ERASE TIME OVER " << tc << " CASES: " << endl << fixed << double(end-begin) / CLOCKS_PER_SEC << endl;

	cout << *rbt.find(123) << endl;

	begin = clock();
	for(int i=0; i<tc; i++){
		rbt.remove(i);
	}

	end = clock();
	cout << "RBT ERASE TIME OVER " << tc << " CASES: " << endl << fixed << double(end-begin) / CLOCKS_PER_SEC << endl;

	

	return 0;
}