#ifndef CALCULATE_EQUATION_H
#define CALCULATE_EQUATION_H

#include "SaveLoadFormula.h"
#include "InsertIntoArray.h"
class CalculateEquation
{
    public:
        CalculateEquation(SaveLoadFormula * SaveLoadFormulaPtr);
        ~CalculateEquation();
        void parseFormulaExpr();
        
    private:
        SaveLoadFormula * m_SaveLoadFormulaPtr;
        InsertIntoArray * m_InsertIntoArrayPtr;
        char * expressionToParse;
        char peek();
        char get();
        int number();
        int factor();
        int term();
        int expression();
};

#endif