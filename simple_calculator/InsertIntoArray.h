#ifndef INSERT_INTO_ARRAY_H
#define INSERT_INTO_ARRAY_H

class InsertIntoArray
{
    public:
        InsertIntoArray(int* originalArray, int positionToInsertAt, int ValueToInsert, int sizeOfOriginalArray);
        ~InsertIntoArray();
        int* insertValue (int* originalArray, int positionToInsertAt, int ValueToInsert, int sizeOfOriginalArray);
        
    private:
        
};

#endif