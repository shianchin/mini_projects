#include "SaveLoadFormula.h"
#include <iostream>
#include <fstream>
#include <string.h>
#include <stdio.h>
using namespace std;

SaveLoadFormula::SaveLoadFormula()
{
    cout << "....DEBUG::SaveLoadFormulaCtor\n";
    //FormulaExpr[30] = {0};
}

SaveLoadFormula::~SaveLoadFormula()
{
    cout << "....DEBUG::SaveLoadFormulaDtor\n";
}

void SaveLoadFormula::WriteToFile(void)
{
    cout << "....DEBUG::WriteToFile\n";
    
    ofstream myfile;
    //string s_FormulaName;
    string s_FormulaExpr;
    
    myfile.open ("formula.txt", ofstream::app);
    
    if (myfile.is_open())
    {
        //cout << "Enter formula name: ";
        //cin >> s_FormulaName;
        
        cout << "Enter formula expression: ";
        cin >> s_FormulaExpr;
        
        //myfile << s_FormulaName << " " << s_FormulaExpr << "\n";
        myfile << s_FormulaExpr << "\n";
        myfile.close();
    }
    else
    {
        cout << "Unable to open file.\n";
    }        
        
    
}

void SaveLoadFormula::ReadFromFile(void)
{
    cout << "....DEBUG::ReadFromFile\n";
    
    string s_FormulaExpr;
    ifstream myfile ("formula.txt");
    
    if (myfile.is_open())
    {
        while ( getline (myfile, s_FormulaExpr) )
        { 
            strncpy(FormulaExpr, s_FormulaExpr.c_str(), sizeof(FormulaExpr));
            FormulaExpr[sizeof(FormulaExpr) - 1] = '\0';
            cout << "....DEBUG::s_FormulaExpr is " << s_FormulaExpr << "\n";
        }
 
        cout << endl;
        myfile.close();
    }
    else
    {
        cout << "File does not exist.\n";
    }          
}

char * SaveLoadFormula::getFormulaExpr(void)
{
    return FormulaExpr;
}
