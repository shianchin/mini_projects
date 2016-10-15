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

#include <string>

class EquationParser
{
public:
    EquationParser();
    ~EquationParser();
    void parseFormulaExpr(std::string eq);
private:
    char * expressionToParse;
    char peek();
    char get();
    double decimal();
    double number();
    double factor();
    double term();
    double expression();
};

#endif
