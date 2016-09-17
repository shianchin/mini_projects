# Diff helper
Using shell script and Python to find the difference between two directories and list down file path of the diff.

##Description
- diff_helper.sh will diff FolderOne and FolderTwo, then list down files that only exist in FolderOne. The output will be saved in diff_raw.txt

   Notes: Only .cpp, .c, and .h will be listed. All unit_test, test_double, mock and fake will be ignored.

```
FolderOne/C++/design_pattern/CH02_strategy/test.cpp
FolderOne/C++/design_pattern/CH02_strategy/test.h
FolderOne/C++/design_pattern/CH03_observer/Milk.cpp -> ../../../../FolderTwo/GitHub/programming_etudes/design_pattern/CH04_decorator/Milk.cpp
FolderOne/C++/design_pattern/CH03_observer/Milk.h -> ../../../../FolderTwo/GitHub/programming_etudes/design_pattern/CH04_decorator/Milk.h
FolderOne/C++/design_pattern/onetwothree/innownoq.cpp
FolderOne/C++/design_pattern/onetwothree/innownoq.h
FolderOne/C++/design_pattern/onetwothree/Observer.h -> ../../../../FolderTwo/GitHub/programming_etudes/design_pattern/CH03_observer/Observer.h
FolderOne/C++/design_pattern/onetwothree/src/iwamgvsefq.cpp
FolderOne/C++/design_pattern/onetwothree/src/iwamgvsefq.h
```
- diff_helper.py is used to execute diff_helper.sh and format the output into CSV.
   
   Notes: Files under same directory are grouped together.
```
FolderOne/C++/design_pattern/CH02_strategy,test.cpp
,test.h
FolderOne/C++/design_pattern/CH03_observer,Milk.cpp ,-> ../../../../FolderTwo/GitHub/programming_etudes/design_pattern/CH04_decorator/Milk.cpp
,Milk.h ,-> ../../../../FolderTwo/GitHub/programming_etudes/design_pattern/CH04_decorator/Milk.h
FolderOne/C++/design_pattern/onetwothree,innownoq.cpp
,innownoq.h
,Observer.h ,-> ../../../../FolderTwo/GitHub/programming_etudes/design_pattern/CH03_observer/Observer.h
FolderOne/C++/design_pattern/onetwothree/src,iwamgvsefq.cpp
,iwamgvsefq.h
```
