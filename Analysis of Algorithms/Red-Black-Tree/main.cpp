#include "rbt.h"
	
using namespace std;

int main(){
	rb <int> t;
	t.insert(5);
	t.insert(4);
	int k = *t.find(5);
	cout << k << endl;
	return 0;
}