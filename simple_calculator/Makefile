CPP      = g++.exe
OBJ      = calculator_main.o \
           InsertIntoArray.o \
           CalculateEquation.o\
           SaveLoadFormula.o
INCS     = CalculateEquation.cpp \
           SaveLoadFormula.cpp \
           InsertIntoArray.cpp
BIN      = calculator_main.exe
RM       = rm.exe -f

$(BIN): $(OBJ)
	$(CPP) calculator_main.o -o calculator_main.exe $(INCS)

calculator_main.o : calculator_main.cpp
	$(CPP) -c calculator_main.cpp -o calculator_main.o

InsertIntoArray.o : InsertIntoArray.cpp
	$(CPP) -c InsertIntoArray.cpp -o InsertIntoArray.o

CalculateEquation.o : CalculateEquation.cpp InsertIntoArray.cpp
	$(CPP) -c CalculateEquation.cpp -o CalculateEquation.o 

SaveLoadFormula.o : SaveLoadFormula.cpp
	$(CPP) -c SaveLoadFormula.cpp -o SaveLoadFormula.o



.PHONY : clean
clean :
		${RM} $(OBJ) $(BIN)