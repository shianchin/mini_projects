#!/usr/bin/env bash
#----------------------------------------------------------------------
# Project           : Replace class name
#
# File name         : replace.sh
#
# Author            : Cheang Shian Chin
#
# Date created      : 25 August 2017
#
# Purpose           : Quick way to change and replace CPP class name.
#
#----------------------------------------------------------------------

#The renaming has no safeguards except the --no-act option.  If the
#user has permission to rewrite file names, the command will perform
#the action without any questions.  For example, the result can be
#quite drastic when the command is run as root in the /lib directory.
#Always make a backup before running the command, unless you truly
#know what you are doing.

echo This is a replace script

old_name="$1"
new_name="$2"
path_to_find=${3:-.} # default to ./

found=$(grep -rnw $old_name $path_to_find)  # this grep will be the slowest

if [[ -n $found ]]; then
    colored_found=$(echo "$found" | grep --color=ALWAYS $old_name)
    echo Found the following:
    echo "$colored_found"

    echo

    affected_files=$(echo "$found" | awk -F : '{print $1}' | sort -u)
    echo Files to be modified:
    echo "$affected_files"
fi


old_filenames=($(find . -type f -name $old_name.*))   # for regular files
new_filenames=($(echo "${old_filenames[@]}" | sed "s/$old_name/$new_name/g"))

if [[ "${#old_filenames[@]}" != 0 ]]; then
    echo Files to be renamed:
    for (( i=0; i<${#old_filenames[@]} ; i+=1 )) ; do
        printf "%s rename to %s\n" "${old_filenames[i]}" "${new_filenames[i]}"
    done
fi

old_symlinks=($(find . -name $old_name.* -type l -ls | awk \
    '{printf("%s %s %s\n", $11,$12,$13)}'))   # for symlinks

if [[ "${#old_symlinks[@]}" != 0 ]]; then
    echo
    echo Old symlinks:
    for (( i=0; i<${#old_symlinks[@]} ; i+=3 )) ; do
        echo "${old_symlinks[i]}" "${old_symlinks[i+1]}" "${old_symlinks[i+2]}"
    done

    echo

    new_symlinks=($(echo "${old_symlinks[@]}" | sed "s/$old_name/$new_name/g"))
    echo New symlinks:
    for (( i=0, j=0; i<${#new_symlinks[@]} ; i+=3,j+=1 )) ; do
        echo "${new_symlinks[i]}" "${new_symlinks[i+1]}" "${new_symlinks[i+2]}"
        new_symlinks_dest[j]="${new_symlinks[i]}"
        new_symlinks_source[j]="${new_symlinks[i+2]}"
    done
fi

echo

while true; do
    read -p "Replace '$old_name' with '$new_name'? [Y/N] " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "Replacing..."
echo "$colored_found" | sed "s/$old_name/$new_name/g"   # just for console display

# actual replace
echo "$affected_files" | xargs sed -i "s/$old_name/$new_name/g" \

# actual rename
if [[ "${#old_filenames[@]}" != 0 ]]; then
    for (( i=0; i<${#old_filenames[@]} ; i+=1 )) ; do
        mv -v "${old_filenames[i]}" "${new_filenames[i]}"
        #sed "p;s/"${old_filenames[i]}"/$new_name/" | xargs -n2 mv
    done
fi

# re-point symlinks
if [[ ${#new_symlinks_dest[@]} != 0 ]]; then
    for (( i=0; i<${#new_symlinks_dest[@]} ; i+=1 )) ; do
        ln -sfn -v "${new_symlinks_source[i]}" "${new_symlinks_dest[i]}"
    done
fi

echo "Done"

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 25-Aug-2017    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------
