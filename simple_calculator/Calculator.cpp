//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : Calculator.cpp
//
// Author            : Cheang Shian Chin
//
// Date created      : 3 June 2016
//
// Purpose           : A simple customizable scientific calculator
//
//----------------------------------------------------------------------

#include <iostream>
#include "Formula.h"
#include "EquationParser.h"
#include "Polynomial.h"

using namespace std;

void userDefinedFormula(void);
void loadFormula(void);
void parseFormula(string equation);
void addFormula(void);
void handlePolynomials(void);

int main()
{
    int userOption = 0;

    while (userOption != 5)
    {
        cout << "\nPlease choose an option.."
             << "\n 1 - Use calculator with user input"
             << "\n 2 - Use calculator with loaded formula"
             << "\n 3 - Add new formula to file"
             << "\n 4 - Polynomials calculation"
             << "\n 5 - Exit"
             << "\nOption = ";

        cin >> userOption;
        cout << endl;

        switch (userOption)
        {
            case 1:
                userDefinedFormula();
                break;
            case 2:
                loadFormula();
                break;
            case 3:
                addFormula();
                break;
            case 4:
                handlePolynomials();
                break;
            case 5:
                // exit
                break;
            default:
                cout << "Invalid operation. Please try again.\n";
                break;
        }
    }

    return 0;
}

void userDefinedFormula()
{
    cout << "*******************************************************************\n"
         << "*  Equation variables can be anything from a to z or A to Z.      *\n"
         << "*  All objects of the equation must NOT be separated by [space].  *\n"
         << "*  e.g. '2 pow r * pi - 10'. TODO:update description              *\n"
         << "*******************************************************************\n"
         << "\nInput equation : ";
    string eq;
    cin >> eq;
    parseFormula(eq);
}

void loadFormula(void)
{
    Formula formula;
    if (formula.loadFromFile())
    {
        cout << "Formulas loaded from file\n";
        cout << "Please choose an option..\n";

        int maxFormula = 0;
        for(int i = 0; !formula.getName(i).empty(); i++ )
        {
            cout << (i+1) << ") "<< formula.getName(i) << endl;
            maxFormula = i;
        }

        cout << "Option = ";

        int userOption = 0;
        cin >> userOption;
        cout << endl;
        if( userOption > 0 && userOption <= (maxFormula+1) )
        {
            string eq = formula.getEquation(userOption-1);
            parseFormula(eq);
        }
        else
        {
            cout << "Option out of range. Please re-input.\n";
            loadFormula();
        }
    }
}

void parseFormula(string equation)
{
    EquationParser parser;
    parser.parseFormulaExpr(equation);
}

void addFormula(void)
{
    Formula formula;
    string fName;
    string equation;

    cout << "Enter formula name: ";
    cin >> fName;

    cout << "Enter formula expression: ";
    cin >> equation;

    formula.writeToFile(fName, equation);
}

void handlePolynomials(void)
{
    Polynomial poly;
}


//----------------------------------------------------------------------
// Revision History  :
//
// Date           Author       Ref    Revision
// 06-Jun-2016    shianchin    1      Initial creation.
//
//----------------------------------------------------------------------
