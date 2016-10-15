//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : Formula.h
//
// Author            : Cheang Shian Chin
//
// Date created      : 15 October 2016
//
// Purpose           : Handles read & write formulae to file.
//
//----------------------------------------------------------------------

#ifndef FORMULA_H
#define FORMULA_H

#include <string>
using namespace std;

typedef struct
{
    string fName;
    string equation;
} formula_t;

class Formula
{
public:
    Formula();
    ~Formula();
    void writeToFile(string fName, string equation);
    bool loadFromFile(void);
    string getName(int index);
    string getEquation(int index);
private:
    formula_t m_formulae[10];  // room for 10 equations
};

#endif
