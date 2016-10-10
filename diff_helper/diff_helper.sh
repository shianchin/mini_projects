#!/usr/bin/env sh
#----------------------------------------------------------------------
# Project           : Diff Helper
#
# File name         : diff_helper.sh
#
# Author            : Cheang Shian Chin
#
# Date created      : 17 September 2016
#
# Purpose           : Diff two dirs, filter only .cpp, .c, and .h, find
#                     out where the symlinks point to.
#
#----------------------------------------------------------------------

# Finding files diff (.cpp .c .h)
# Only in FolderOne
diff -qr FolderOne/C++/design_pattern/ FolderTwo/GitHub/programming_etudes/design_pattern/ > diff_raw.txt
cat diff_raw.txt | grep "Only in FolderOne" | grep -vi "unit_test\|test_double\|fake\|mock\|stub" | awk '{print $3$4}' | sed 's/://' > diff_code_only.txt
> diff_result.txt

findSymlink()
{
  printf '%s\n' "$1" | while IFS= read -r line
  do
    if [ ! -L "$line" ]; then
      #echo "=> is file!    $line"
      echo "$line" >> diff_result.txt
    else
      local SYMLINK="$(ls -l $line | awk '{printf ("%s %s\n", $10, $11)}' | sed 's/*//')"
      #echo "=> is symlink! $line" $SYMLINK
      echo "$line" $SYMLINK >> diff_result.txt
    fi
  done
}

FILE_PATH="$(cat diff_code_only.txt | grep "\.[ch]" | sed 's_:_/_')"
findSymlink "$FILE_PATH"
FILE_PATH="$(cat diff_code_only.txt | grep -v "\.[ch]"  | find $(sed 's/://') -name "*.*" | grep -vi "unit_test\|test_double\|fake\|mock\|stub" | grep "\.[ch]")"
findSymlink "$FILE_PATH"
FILE_PATH="$(cat diff_raw.txt | grep "differ" | grep -vi "unit_test\|test_double\|fake\|mock\|stub" | grep "\.[ch]" | awk '{print $2}')"
findSymlink "$FILE_PATH"

sort diff_result.txt -o diff_result.txt

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 10-Oct-2016    shianchin    2      Save results in temp files.
# 17-Sep-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------
