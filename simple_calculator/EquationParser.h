//----------------------------------------------------------------------
// Project           : Customizable Scientific Calculator
//
// File name         : EquationParser.h
//
// Author            : Cheang Shian Chin
//
// Date created      : 15 October 2016
//
// Purpose           : Parsing equation using recursive descent parser.
//
//----------------------------------------------------------------------

#ifndef EQUATION_PARSER_H
#define EQUATION_PARSER_H

#include "Formula.h"
#include "InsertIntoArray.h"
class EquationParser
{
public:
    EquationParser(Formula * SaveLoadFormulaPtr);
    ~EquationParser();
    void parseFormulaExpr();

private:
    Formula * m_SaveLoadFormulaPtr;
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
