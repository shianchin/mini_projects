//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : EquationParser.cpp
//
// Author            : Cheang Shian Chin
//
// Date created      : 15 October 2016
//
// Purpose           : Parsing equation using recursive descent parser.
//
//----------------------------------------------------------------------

#include "EquationParser.h"
#include <iostream>
#include <string.h>  // Bash on Ubuntu on Windows is weirding out
using namespace std;

EquationParser::EquationParser()
{
}

EquationParser::~EquationParser()
{
}

void EquationParser::parseFormulaExpr(string eq)
{
    cout << "\nThe original equation is : " << eq << endl;

    size_t f = eq.find("pi");
    if (f!=string::npos)
    {
        eq.replace(f, string("pi").length(), "3.14");  //3.14159
    }

    //Getting input for variables
    size_t found = eq.find_first_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
    while (found!=string::npos)
    {
        cout << "Please input value for variable " << eq[found] << " : ";
        string val;
        cin >> val;
        eq.replace(found, string(val).length(), val);
        found = eq.find_first_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",found+1);
    }

    // convert string to char*
    char c_eq[eq.size()+1];  // plus null
    strcpy(c_eq, eq.c_str());
    expressionToParse = c_eq;

    double result = expression();

    cout << "\n  " << eq << " = " << result << endl;
}

// Below codes are recursive descent parser mostly copied from internet.
char EquationParser::peek()
{
    return *expressionToParse;
}

char EquationParser::get()
{
    return *expressionToParse++;
}

// TODO: Handle exponent

double EquationParser::floating()
{
    // TODO: Handle more than 2 decimal places
    double result = get() - '0';

    while (peek() >= '0' && peek() <= '9')
    {
        result = result/10.0 + (get() - '0')/100.0;
    }
    return result;
}

double EquationParser::number()
{
    double result = get() - '0';

    while (peek() >= '0' && peek() <= '9')
    {
        result = 10*result + get() - '0';
    }

    if (peek() == '.')
    {
        get();
        result = result + floating();
    }

    return result;
}

double EquationParser::factor()
{
    if (peek() >= '0' && peek() <= '9')
    {
        return number();
    }
    else if (peek() == '(')
    {
        get(); // '('
        double result = expression();
        get(); // ')'
        return result;
    }
    else if (peek() == '-')
    {
        get();
        return -factor();
    }

    return 0; // error
}

double EquationParser::term()
{
    double result = factor();

    while (peek() == '*' || peek() == '/')
    {
        if (get() == '*')
            result *= factor();
        else
            result /= factor();
    }

    return result;
}

double EquationParser::expression()
{
    double result = term();

    while (peek() == '+' || peek() == '-')
    {
        if (get() == '+')
            result += term();
        else
            result -= term();
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
