
#ifndef SAVELOADFORMULA_H
#define SAVELOADFORMULA_H
#include <stdio.h>
#include <string.h>


class SaveLoadFormula
{
    public:
        SaveLoadFormula();
        ~SaveLoadFormula();
        void WriteToFile(void);
        void ReadFromFile(void);
        char * getFormulaExpr(void);
        
    private:
        char FormulaExpr[30];
};

#endif
