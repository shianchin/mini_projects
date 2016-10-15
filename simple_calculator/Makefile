CPP=g++
EXE=Calculator
SRC=\
	Calculator.cpp \
	EquationParser.cpp \
	Formula.cpp \
	Polynomial.cpp \

.PHONY: all
all: $(EXE) run

$(EXE): $(SRC)
	$(CPP) $(SRC) -o $(EXE)

.PHONY: run
run:
	./$(EXE)

.PHONY: clean
clean:
	rm -f $(EXE)
