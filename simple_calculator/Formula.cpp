//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : Formula.cpp
//
// Author            : Cheang Shian Chin
//
// Date created      : 15 October 2016
//
// Purpose           : Handles read & write formulae to file.
//
//----------------------------------------------------------------------

#include "Formula.h"
#include <string.h>
#include <iostream>
#include <fstream>
using namespace std;

Formula::Formula()
{
}

Formula::~Formula()
{
}

void Formula::writeToFile(string fName, string equation)
{
    ofstream myfile("formula.txt", ofstream::app);  //append to file

    if (myfile.is_open())
    {
        myfile << fName << "\n" << equation << "\n";
        myfile.close();
        cout << "> Formula written successful!\n";
    }
    else
    {
        cout << "Unable to open file.\n";
    }
}

bool Formula::loadFromFile(void)
{
    bool isFileExist = false;
    string s_FormulaExpr;
    ifstream myfile("formula.txt");

    if (myfile.is_open())
    {
        int i = 0;
        int lineNum = 0;
        string fName;
        char* comma = 0;
        while ( getline(myfile, s_FormulaExpr) )
        {
            if (lineNum%2 == 0)  // first line is formula name
            {
                m_formulae[i].fName = s_FormulaExpr;
            }
            else  // second line is formula equation
            {
                m_formulae[i].equation = s_FormulaExpr;
                i++;
            }
            lineNum++;
        }
        myfile.close();
        isFileExist = true;
    }
    else
    {
        cout << "File does not exist.\n";
        isFileExist = false;
    }
    return isFileExist;
}

string Formula::getName(int index)
{
    return m_formulae[index].fName;
}

string Formula::getEquation(int index)
{
    return m_formulae[index].equation;
}


//----------------------------------------------------------------------
// Revision History  :
//
// Date           Author       Ref    Revision
// 15-Oct-2016    shianchin    1      Initial creation.
//
//----------------------------------------------------------------------
