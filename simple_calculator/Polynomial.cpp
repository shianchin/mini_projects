//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : Polynomial.cpp
//
// Author            : Cheang Shian Chin
//
// Date created      : 15 October 2016
//
// Purpose           : Handles polynomials calculation.
//
//----------------------------------------------------------------------

#include "Polynomial.h"
#include <cmath>
#include <string.h>
#include <iostream>
using namespace std;

Polynomial::Polynomial()
{
    //struct poly_t m_poly;
}

Polynomial::~Polynomial()
{
}

void Polynomial::setPoly()
{
    m_poly.numTerm = 0;
    cout << "Enter number of polynomial terms (max 10): ";
    cin >> m_poly.numTerm;

    for (int i = 0; i < m_poly.numTerm; i++)
    {
        cout << "\nEnter coefficient: ";
        cin >> m_poly.coeff[i];
        cout <<"Enter exponent: ";
        cin >> m_poly.exp[i];
    }
    cout << "\n> Polynomial entered success!" << endl;
}

ostream& operator<<(ostream &output, const Polynomial &p)
{
    for (int i = 0; i < p.m_poly.numTerm; i++)
    {
        if (i == (p.m_poly.numTerm - 1)) // for last term
        {
            if (p.m_poly.exp[ i ] > 1) // if power greater than one
                output << p.m_poly.coeff[ i ] << "x^" << p.m_poly.exp[ i ];
            if (p.m_poly.exp[ i ] == 1) // if power equal to one
                output << p.m_poly.coeff[ i ] << "x";
        }
        else // for the rest of the terms
        {
            if (p.m_poly.coeff[ i+1 ] > 0 && p.m_poly.exp[ i ] != 1) // NEXT term is positive & CURRENT term power not one
                output << p.m_poly.coeff[ i ] << "x^" << p.m_poly.exp[ i ]<<"+";
            if (p.m_poly.coeff[ i+1 ] > 0 && p.m_poly.exp[ i ] == 1) // NEXT term is positive & CURRENT term power equal one
                output << p.m_poly.coeff[ i ] << "x" << "+";
            if (p.m_poly.coeff[ i+1 ] < 0 && p.m_poly.exp[ i ] != 1) // NEXT term is negative & CURRENT term power not one
                output << p.m_poly.coeff[ i ] << "x^" << p.m_poly.exp[ i ];
            if (p.m_poly.coeff[ i+1 ] < 0 && p.m_poly.exp[ i ] == 1) // NEXT term is negative & CURRENT term power equal one
                output << p.m_poly.coeff[ i ] << "x";
        }
    }
    return output;
}
/*
string Polynomial::toString(void)
{
    string p_str;
    for (int i = 0; i < m_poly.numTerm; i++)
    {
        if (i == (m_poly.numTerm - 1)) // for last term
        {
            if (m_poly.exp[ i ] > 1) // if power greater than one
                p_str = m_poly.coeff[ i ] + "x^" + m_poly.exp[ i ];
            if (m_poly.exp[ i ] == 1) // if power equal to one
                p_str = m_poly.coeff[ i ] + "x";
        }
        else // for the rest of the terms
        {
            if (m_poly.coeff[ i+1 ] > 0 && m_poly.exp[ i ] != 1) // NEXT term is positive & CURRENT term power not one
                p_str = m_poly.coeff[ i ] + "x^" + m_poly.exp[ i ] + "+";
            if (m_poly.coeff[ i+1 ] > 0 && m_poly.exp[ i ] == 1) // NEXT term is positive & CURRENT term power equal one
                p_str = m_poly.coeff[ i ] + "x" + "+";
            if (m_poly.coeff[ i+1 ] < 0 && m_poly.exp[ i ] != 1) // NEXT term is negative & CURRENT term power not one
                p_str = m_poly.coeff[ i ] + "x^" + m_poly.exp[ i ];
            if (m_poly.coeff[ i+1 ] < 0 && m_poly.exp[ i ] == 1) // NEXT term is negative & CURRENT term power equal one
                p_str = m_poly.coeff[ i ] + "x";
        }
    }
    return p_str;
}
*/
// TODO: + and - not correct when numTerm of A & B are not same
Polynomial Polynomial::operator+(const Polynomial& p)
{
    Polynomial poly;
    int k = 0;

    for (int i = 0; i < this->m_poly.numTerm; i++) // add polynomial A & B
    {
        for (int j = 0; j < p.m_poly.numTerm; j++)
        {
            if (this->m_poly.exp[ i ] == p.m_poly.exp[ j ])
            {
                poly.m_poly.coeff[ k ] = this->m_poly.coeff[ i ] + p.m_poly.coeff[ j ];
                poly.m_poly.exp[ k ] = this->m_poly.exp[ i ];
                k++;
                poly.m_poly.numTerm = k;
            }
        }
    }
    return poly;
}

Polynomial Polynomial::operator-(const Polynomial& p)
{
    Polynomial poly;
    int k = 0;

    for (int i = 0; i < this->m_poly.numTerm; i++) // subtract polynomial B from A
    {
        for (int j = 0; j < p.m_poly.numTerm; j++)
        {
            if (this->m_poly.exp[ i ] == p.m_poly.exp[ j ])
            {
                poly.m_poly.coeff[ k ] = this->m_poly.coeff[ i ] - p.m_poly.coeff[ j ];
                poly.m_poly.exp[ k ] = this->m_poly.exp[ i ];
                k++;
                poly.m_poly.numTerm = k;
            }
        }
    }
    return poly;
}

double Polynomial::calculate(double x)
{
    double result = 0;

    // calculate polynomial p
    for (int i = 0; i < this->m_poly.numTerm; i++)
    {
        result += this->m_poly.coeff[ i ] * pow(x, this->m_poly.exp[ i ]);
    }
    return result;
}

//----------------------------------------------------------------------
// Revision History  :
//
// Date           Author       Ref    Revision
// 15-Oct-2016    shianchin    1      Initial creation.
//
//----------------------------------------------------------------------
