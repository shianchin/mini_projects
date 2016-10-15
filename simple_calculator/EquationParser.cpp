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
#include "Formula.h"
#include "InsertIntoArray.h"
#include <iostream>
using namespace std;

EquationParser::EquationParser(Formula * SaveLoadFormulaPtr)
{
    m_SaveLoadFormulaPtr = SaveLoadFormulaPtr;
    cout << "....DEBUG::CalculateEquationCtor\n";
}

EquationParser::~EquationParser()
{
    cout << "....DEBUG::CalculateEquationDtor\n";
}

void EquationParser::parseFormulaExpr()
{
    cout << "....DEBUG::Entering parseFormulaExpr\n";

    expressionToParse = m_SaveLoadFormulaPtr->getFormulaExpr();

    for (int i = 0; expressionToParse[i] != '\0'; i++)
        cout << "....DEBUG::expressionToParse [" << i << "] = " << expressionToParse[i] << endl;


    //Getting input for variables
    for (int i = 0; expressionToParse[i] != '\0'; i++)
    {
        if ( ((int)expressionToParse[i] >= 65 && (int)expressionToParse[i] <= 90) ||
             ((int)expressionToParse[i] >= 97 && (int)expressionToParse[i] <= 122)   )    //A to Z and a to z
        {
            cout << "Please input value for variable " << expressionToParse[i] << " : ";
            char input_temp[10];
			cin >> input_temp[0];

            int x[5]={0, 1, 2, 3, 4};
            m_InsertIntoArrayPtr = new InsertIntoArray(x,3,7,5);
            //int* z = m_InsertIntoArrayPtr->insertValue(x,3,7,5);
            cout << "....DEBUG::input_temp = " << input_temp << endl;
            //cout << "....DEBUG::z = " << z << endl;
            //cin >> expressionToParse[i];
            //delete[] z;
            delete m_InsertIntoArrayPtr;
        }
    }

    for (int i = 0; expressionToParse[i] != '\0'; i++)
        cout << "....DEBUG::expressionToParse [" << i << "] = " << expressionToParse[i] << endl;

    int result = expression();
    cout << "result = " << result << endl;
}

// Below codes are recursive descent parser copied from internet.
char EquationParser::peek()
{
    return *expressionToParse;
}

char EquationParser::get()
{
    return *expressionToParse++;
}

int EquationParser::number()
{
    int result = get() - '0';

    while (peek() >= '0' && peek() <= '9')
    {
        result = 10*result + get() - '0';
    }

    return result;
}

int EquationParser::factor()
{
    if (peek() >= '0' && peek() <= '9')
    {
        return number();
    }
    else if (peek() == '(')
    {
        get(); // '('
        int result = expression();
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

int EquationParser::term()
{
    int result = factor();

    while (peek() == '*' || peek() == '/')
    {
        if (get() == '*')
            result *= factor();
        else
            result /= factor();
    }

    return result;
}

int EquationParser::expression()
{
    int result = term();

    while (peek() == '+' || peek() == '-')
    {
        if (get() == '+')
            result += term();
        else
            result -= term();
    }

    return result;
}
