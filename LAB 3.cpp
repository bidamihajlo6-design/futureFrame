#include <iostream>
#include <cmath>
#include <string>
using namespace std;

int main()
{
	double a, b, c;

	while (true) {
		cout << "Enter the coefficients a,b,c (separeted by a space):";

		cin >> a
			>> b
			>> c;

		cout << "a: " << a << ", b: " << b << ", c: " << c << endl;
		double D = b * b - 4 * a * c;

		cout << "D = " << D << endl;

		if (D > 0) {
			double x1 = (-b + sqrt(D)) / (2 * a);
			double x2 = (-b - sqrt(D)) / (2 * a);
			cout << "x1 = " << x1 << ", x2 = " << x2 << endl;
		}
		else if (D == 0) {
			double x = -b / (2 * a);
			cout << "x = " << x << endl;
		}
		else {
			cout << "No real roots" << endl;
		}
		char choise;
		cout << "\n Want to solve another quathion? (y/n)";
		cin >> choise;

		if (choise != 'y' && choise != 'Y') {
			cout << "Completing the program..." << endl;
			break;
		}
	} cout << "\n--------------------------\n";


	
	return 0;
}
