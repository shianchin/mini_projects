//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : Polynomial.h
//
// Author            : Cheang Shian Chin
//
// Date created      : 15 October 2016
//
// Purpose           : Handles polynomials calculation.
//
//----------------------------------------------------------------------

#ifndef POLYNOMIAL_H
#define POLYNOMIAL_H

#include <string>
using namespace std;

class Polynomial
{
public:
    Polynomial(void);
    ~Polynomial(void);
    void setPoly(void);
    // Overload << operator to display Poly object.
    friend ostream& operator<<(ostream &output, const Polynomial &p);
    //string toString(void);  // TODO: return string to let EquationParser handle
    // Overload + operator to add two Poly objects.
    Polynomial operator+(const Polynomial& p);
    // Overload - operator to subtract two Poly objects.
    Polynomial operator-(const Polynomial& p);
    double calculate(double x);
private:
    struct poly_t
    {
        int numTerm;
        double coeff[10];
        int exp[10];
    };
    poly_t m_poly;
};

#endif
