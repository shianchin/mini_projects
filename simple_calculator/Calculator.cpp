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
#include <iterator>
#include "Formula.h"
//#include "CalculateEquation.h"

using namespace std;

void function_1();
void loadFormula(void);
void addFormula(void);

int main()
{
    int userOption = 0;

    do{
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
                function_1();  // TODO
                break;
            case 2:
                loadFormula();
                break;
            case 3:
                addFormula();
                break;
            case 4:
                cout << "case 4";  // TODO
                break;
            case 5:
                break;
            default:
                cout << "Invalid operation. Please try again.\n";
                break;
        }
    } while (userOption != 5);

    return 0;
}

void function_1()
{
    cout << "***************************************************************\n"
         << "*  Equation variables can be anything from a to z or A to Z.  *\n"
         << "*  All objects of the equation must be separated by [space].  *\n"
         << "*  e.g. '2 pow r * pi - 10'.                                  *\n"
         << "***************************************************************\n"
         << "\nEnter your equation: ";
}

void loadFormula()
{
    Formula formula;
    if (formula.loadFromFile())
    {
        cout << "Formulas loaded from file\n";
        cout << "Please choose an option..\n";

        for(int i = 0; !formula.getName(i).empty(); i++ )
        {
            cout << (i+1) << ") "<< formula.getName(i) << endl;
        }

        cout << "Option = ";

        int userOption = 0;
        cin >> userOption;
        cout << endl;
        cout << "The original equation is : " << formula.getEquation(userOption-1) << endl;
    }
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


//----------------------------------------------------------------------
// Revision History  :
//
// Date           Author       Ref    Revision
// 06-Jun-2016    shianchin    1      Initial creation.
//
//----------------------------------------------------------------------
