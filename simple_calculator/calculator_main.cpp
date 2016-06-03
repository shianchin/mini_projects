#include <iostream>
#include "SaveLoadFormula.h"
#include "CalculateEquation.h"

using namespace std;

void function_1();
void function_2();
void function_3();

int main()
{
    int userOption = 0;
    
    do{
        cout << "\nPlease select an option."
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
                function_1();
                break;
                
            case 2:
                function_2();
                break;
                
            case 3:
                function_3();
                break;
                
            case 4:
                cout << "case 4";
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

void function_2()
{
    SaveLoadFormula * SaveLoadFormulaPtr;
    CalculateEquation * CalculateEquationPtr;

    
    SaveLoadFormulaPtr = new SaveLoadFormula();
    CalculateEquationPtr = new CalculateEquation(SaveLoadFormulaPtr);
    SaveLoadFormulaPtr->ReadFromFile();


    CalculateEquationPtr->parseFormulaExpr();
    delete SaveLoadFormulaPtr;
    delete CalculateEquationPtr;
}

void function_3()
{
    SaveLoadFormula * SaveLoadFormulaPtr;
    SaveLoadFormulaPtr = new SaveLoadFormula();
    SaveLoadFormulaPtr->WriteToFile();
    delete SaveLoadFormulaPtr;
}
