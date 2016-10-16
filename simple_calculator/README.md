# Customizable Scientific Calculator
The objective of this assignment is to enhance the skills (designing and programming) of the students to solve problem using the C++ programming language. Students are required to design a Customizable Scientific Calculator.

The customizable calculator must be able to perform the following functions:
* A file to add mathematical formulas (Example: circumference and area of a circle)
* Calculate basic mathematical functions (x + y, x - y, x / y, x * y, x pow y)
* Able to retrieve the mathematical formula stored in the text file for calculation
* Able to accept decimal and floating-point inputs
* Must be able to calculate any amount of variables
* Able to accept variable in place of decimal values when inputting formula equation (Example: a + a + 10) and later on identify the variables before asking for user input


The calculator should also handle Polynomial Calculation as follows:

The internal representation of a Polynomial is an array of terms. Each term contains a coefficient and an exponent. The term 2x<sup>4</sup> has the coefficient 2 and the exponent 4.

##Capabilities

a) The addition operator (+) to add two Polynomials.

b) The subtraction operator (-) to subtract two Polynomials.

c) The assignment operator to assign one Polynomial to another.

d) The addition assignment operator (+=) and subtraction assignment operator (-=).

e) Able to accept input of the variable to calculate the overall value of the equation.

##Program Output 1
```
Please choose an option..
 1 - Use calculator with user input
 2 - Use calculator with loaded formula
 3 - Add new formula to file
 4 - Polynomials calculation
 5 - Exit
Option = 2

File does not exist.

Please choose an option..
 1 - Use calculator with user input
 2 - Use calculator with loaded formula
 3 - Add new formula to file
 4 - Polynomials calculation
 5 - Exit
Option = 3

Enter formula name: circumference
Enter formula expression: 2*pi*r
> Formula written successful!

Please choose an option..
 1 - Use calculator with user input
 2 - Use calculator with loaded formula
 3 - Add new formula to file
 4 - Polynomials calculation
 5 - Exit
Option = 2

Formulas loaded from file
Please choose an option..
1) circumference
Option = 1

The original equation is : 2*pi*r
```
##Program Output 2
```
Please choose an option..
 1 - Use calculator with user input
 2 - Use calculator with loaded formula
 3 - Add new formula to file
 4 - Polynomials calculation
 5 - Exit
Option = 4

Enter number of polynomial terms (max 10): 3

Enter coefficient: 12
Enter exponent: 1

Enter coefficient: 4
Enter exponent: 2

Enter coefficient: 6
Enter exponent: 3

> Polynomial entered success!
Enter number of polynomial terms (max 10): 3

Enter coefficient: -5
Enter exponent: 1

Enter coefficient: 3
Enter exponent: 2

Enter coefficient: 1
Enter exponent: 3

> Polynomial entered success!
1st polynomial is:
12x+4x^2+6x^3

2nd polynomial is:
-5x+3x^2+1x^3

Adding the polynomials yields:
7x+7x^2+7x^3

Subtracting the polynomials yields:
17x+1x^2+5x^3

Enter the value of x: 2
7x+7x^2+7x^3 = 98
17x+1x^2+5x^3 = 78
```
