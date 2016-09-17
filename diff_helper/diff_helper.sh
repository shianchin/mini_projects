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
DIFF_RAW="$(diff -qr FolderOne/C++/design_pattern/ FolderTwo/GitHub/programming_etudes/design_pattern/)"
DIFF_DL_ONLY="$(echo "${DIFF_RAW}" | \
                 grep "Only in FolderOne" | \
                 grep -vi "unit_test\|test_double\|fake\|mock" | \
                 awk '{print $3$4}')"
> diff_raw.txt
findSymlink()
{
  printf '%s\n' "$1" | while IFS= read -r line
  do
    if [ ! -L "$line" ]; then
      echo "=> is file!    $line"
      echo "$line" >> diff_raw.txt
    else
      local SYMLINK="$(ls -l $line | awk '{printf ("%s %s\n", $10, $11)}' | sed 's/*//')"
      echo "=> is symlink! $line" $SYMLINK
      echo "$line" $SYMLINK >> diff_raw.txt
    fi
  done
}

FILE_PATH="$(echo "${DIFF_DL_ONLY}" | grep "\.[ch]" | sed 's_:_/_')"
findSymlink "$FILE_PATH"
FILE_PATH="$(echo "${DIFF_DL_ONLY}" | grep -v "\.[ch]" | find $(sed 's/://') -name "*.*" | grep "\.[ch]")"
findSymlink "$FILE_PATH"

sort diff_raw.txt

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 17-Sep-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------
