#include "InsertIntoArray.h"
#include <iostream>
using namespace std;

InsertIntoArray::InsertIntoArray(int* originalArray, int positionToInsertAt, int ValueToInsert, int sizeOfOriginalArray)
{
    cout << "....DEBUG::InsertIntoArrayCtor\n";
}

InsertIntoArray::~InsertIntoArray()
{
    cout << "....DEBUG::InsertIntoArrayDtor\n";
}

int* insertValue (int* originalArray, int positionToInsertAt, int ValueToInsert, int sizeOfOriginalArray)
{
  // Create the new array - user must be told to delete it at some point
  int* newArray = new int[sizeOfOriginalArray + 1];

  
  for (int i=0; i<=sizeOfOriginalArray; ++i)
  {
    if (i < positionToInsertAt)  // All the elements before the one that must be inserted
    {
       newArray[i] = originalArray[i];
    }
  
    if (i == positionToInsertAt)  // The right place to insert the new element
    {
      newArray[i] = ValueToInsert;
    }
 
    if (i > positionToInsertAt)  // Now all the remaining elements
    {
      newArray[i] = originalArray[i-1];
    }
  }
return newArray;
}