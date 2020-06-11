#include <iostream>
#include <vector>
#define MAX 2147483647

using namespace std;

enum {RED, BLACK};

template <class T> class rb;

template <class T>
class node{
	node<T> *left, *right, *p;
	int color;
	int w;
	friend class rb<T>;
public:
	T key;
};


template <class T>
class rb{
	node<T> *root, *nil;
	int ncount;
	void left_rotate(node<T> *);
	void right_rotate(node<T> *);
	void insert_fixup(node<T> *);
	void transplant(node<T> *, node<T> *);
	void remove_fixup(node<T> *);
	node<T> *minimum(node<T> *);
	node<T> *init_node(T );
	int dfs(node<T> *);
	void update_counts(node<T> *, int );
	node<T> *find_ptr(T);
public:
	void insert(T );
	void remove(T );
	int count_reds();
	int count_blacks();
	T find_kth_smallest(int, node<T> *);
	T *find(T ); 
	rb(){
		ncount = 0;
		nil = new node<T>;
		nil->color = BLACK;
		nil->left = nullptr;
		nil->right = nullptr;
		root = nil;
	};
	void test(){
		cout << root->w << endl;
	};
	int size(){ return ncount; };
};


template <class T>
node<T> *rb<T>::init_node(T key){
	node<T> *n = new node<T>;
	n->left = nullptr;
	n->right = nullptr;
	n->p = nullptr;
	n->color = RED;
	n->key = key;
	n->w = 0;
	return n;
};

template <class T>
T *rb<T>::find(T key){
	node<T> *n = root;
	while(n != nil){
		if(key == n->key) return &n->key;
		if(key < n->key)
			n = n->left;
		else n = n->right;
	}
	return nullptr;
}

template <class T>
node<T> *rb<T>::find_ptr(T key){
	node<T> *n = root;
	while(n != nil){
		if(key == n->key) return n;
		if(key < n->key)
			n = n->left;
		else n = n->right;
	}
	return nullptr;
}

template <class T>
node<T> *rb<T>::minimum(node<T> *n){
	while(n->left != nil)
		n = n->left;
	return n;
}


template <class T>
void rb<T>::left_rotate(node<T> *n){
	node<T> *y = n->right;
	n->w -= y->right->w + 1;
	y->w += n->left->w + 1;

	n->right = y->left;
	if(y->left != nil){
		y->left->p = n; // turn y's subtree into x's subtree
	}
	// link the parent of the y to parent of the x
	
	y->p = n->p;
	if(n->p == nil){
		root = y; 
	}else if(n == n->p->left){
		n->p->left = y;
	}else{
		n->p->right = y;
	}
	
	y->left = n; // y's left subtree's root is now n
	n->p = y; // parent of n is now y
}

template <class T>
void rb<T>::right_rotate(node<T> *n){
	node<T> *y = n->left;
	n->w -= y->left->w + 1;
	y->w += n->right->w + 1;

	n->left = y->right;
	if(y->right != nil){
		y->right->p = n; // turn y's subtree into n's subtree
	}
	
	// link the parent of the y to parent of the n
	y->p = n->p;
	if(n->p == nil){
		root = y; 
	}else if(n == n->p->right){
		n->p->right = y;
	}else{
		n->p->left = y;
	}
	
	y->right = n; // y's right subtree's root is now n
	n->p = y; // parent of n is now y
}

template <class T>
void rb<T>::update_counts(node<T> *n, int val){
	while(n != nil){
		n->w += val;
		n = n->p;
	}
}

template <class T>
void rb<T>::insert(T key){
	node<T> *n = init_node(key);

	node<T> *y = nil;
	node<T> *x = root;
	
	while(x != nil){
		y = x;
		if(n->key < x->key)
			x = x->left;
		else
			x = x->right;
	}
	
	n->p = y;
	if(y == nil)
		root = n;
	else if(n->key < y->key)
		y->left = n;
	else
		y->right = n;

	n->left = nil;
	n->right = nil;
	n->color = RED;
	update_counts(n, 1);
	insert_fixup(n);
	ncount++;
}

template <class T>
void rb<T>::insert_fixup(node<T> *n){
	while(n->p->color == RED){
		if(n->p == n->p->p->left){
			node<T> *y = n->p->p->right; // set y to the uncle of current n
			if(y->color == RED){
				n->p->color = BLACK;
				y->color = BLACK;
				n->p->p->color = RED;
				n = n->p->p;
			}else{
				if(n == n->p->right){
					n = n->p;
					left_rotate(n);
				}
				n->p->color = BLACK;
				n->p->p->color = RED;
				right_rotate(n->p->p);
			}
		}else{
			node<T> *y = n->p->p->left; // set y to the uncle of current n
			if(y->color == RED){
				n->p->color = BLACK;
				y->color = BLACK;
				n->p->p->color = RED;
				n = n->p->p;
			}else{
				if(n == n->p->left){
					n = n->p;
					right_rotate(n);
				}
				n->p->color = BLACK;
				n->p->p->color = RED;
				left_rotate(n->p->p);
			}
		}
	}
	root->color = BLACK;
}

template <class T>
void rb<T>::transplant(node<T> *u, node<T> *v){
	if(u->p == nil)
		root = v;
	else if(u == u->p->left)
		u->p->left = v;
	else
		u->p->right = v;
	v->p = u->p;
}

template <class T>
void rb<T>::remove(T key){
	node<T> *n;
	if(!(n = find_ptr(key))){
		cerr << "Cannot find the node<T> with key = " << key << endl;
		return;
	}

	// node<T> y is to replace node<T> n
	node<T> *y = n;
	// node<T> x is to replace original position of node<T> y
	node<T> *x;
	int y_ori_color = y->color;
	
	if(n->left == nil){
		x = n->right;
		transplant(n, n->right);
	}else if(n->right == nil){
		x = n->left;
		transplant(n, n->left);
	}else{
		y = minimum(n->right);
		y_ori_color = y->color;
		x = y->right;
		if(y->p == n)
			x->p = y;
		else{
			transplant(y, y->right);
			y->right = n->right;
			y->right->p = y;
		}
		transplant(n, y);
		y->left = n->left;
		y->left->p = y;
		y->color = n->color;
	}
	update_counts(n, -1);
	delete n;
	if(y_ori_color == BLACK){
		remove_fixup(x);
	}
	nil->left = nullptr;
	nil->right = nullptr;
	nil->p = nullptr;
	ncount--;
}

template <class T>
void rb<T>::remove_fixup(node<T> *n){
	int ctr = 0;
	while(n != root and n->color == BLACK){
		ctr++;
		if(n == n->p->left){
			node<T> *w = n->p->right; // set w as sibling node<T> of node<T> n
			if(w->color == RED){
				w->color = BLACK;
				n->p->color = RED;
				left_rotate(n->p);
				w = n->p->right;						
			}	
			if(w->left->color == BLACK and w->right->color == BLACK){
				w->color = RED;
				n = n->p;
			}else{
				if(w->right->color == BLACK){
					w->left->color = BLACK;
					w->color = RED;
					right_rotate(w);
					w = n->p->right;
				}
				w->color = n->p->color;
				n->p->color = BLACK;
				w->right->color = BLACK;
				left_rotate(n->p);
				n = root;
			}
		}else{
			node<T> *w = n->p->left; // set w as sibling node<T> of node<T> n
			if(w->color == RED){
				w->color = BLACK;
				n->p->color = RED;
				right_rotate(n->p);
				w = n->p->left;							
			}
			if(w->left->color == BLACK and w->right->color == BLACK){
				w->color = RED;
				n = n->p;
			}else{
				if(w->left->color == BLACK){
					w->right->color = BLACK;
					w->color = RED;
					left_rotate(w);
					w = n->p->left;
				}
				w->color = n->p->color;
				n->p->color = BLACK;
				w->left->color = BLACK;
				right_rotate(n->p);
				n = root;
			}
		}
	}
	n->color = BLACK;
}

template <class T>
int rb<T>::dfs(node<T> *n){
	int sub_reds = 0;
	if(n->left != nil)
		sub_reds += dfs(n->left);
	if(n->right != nil)
		sub_reds += dfs(n->right);
	return sub_reds + (n->color == RED);
}

template <class T>
int rb<T>::count_reds(){
	return dfs(root);
}

template <class T>
int rb<T>::count_blacks(){
	return ncount - count_reds();
}

template <class T>
T rb<T>::find_kth_smallest(int k, node<T> *n){
	if(n == nullptr)
		n = root;

	if(n->left->w >= k) return find_kth_smallest(k, n->left);
	if(n->left->w + 1 == k) return n->key;
	return find_kth_smallest(k-n->left->w-1, n->right);
}


struct package{
	int size, ordinal;
	bool operator<(package other){
		if(size != other.size)
			return size < other.size;
		return ordinal < other.ordinal;
	};
	bool operator>(package other){
		if(size != other.size)
			return size > other.size;
		return ordinal > other.ordinal;
	};
	bool operator==(package other){
		return size == other.size;
	};
	friend ostream& operator<<(ostream& os, package& pc){
		os << pc.size << " " << pc.ordinal << endl;
		return os;
	};
};
