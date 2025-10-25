#include <iostream>
#include <cmath>
#include <string>
using namespace std;
		

int main()
 {
	int a = 10;  
	double b = 5.5;
	float c = 3.2f; 
	string str = "Hello";
	
	a += 5; b *= 2; c -= 1; str += "World";
	cout << "a: " << a << ", b: " << b << ", c: " << c << ", str: " << str << endl;
	
	cout << "sqrt(25)=" << sqrt(25) << endl;
	cout << " pow(2,3)=" << pow(2, 3) << endl;
	cout << "abs(-7)=" << abs(-7) << endl;
	cout << "ceil(3.2) =" << ceil(3.2) << endl;
	cout << "floor(3.8)=" << floor(3.8) << endl;

	cout << "Length: " << str.length() << endl;
	cout << "Substring: " << str.substr(0, 5) << endl;
	cout << "Find 'World': " << str.find("World") << endl;

	return 0;
}