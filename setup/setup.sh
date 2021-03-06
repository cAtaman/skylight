#!/bin/bash

# over-engineered snippet to get directory of running bash script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"


# change to one directory above ( skylight/ )
cd "$DIR"/..
SKYLIGHT_ROOT="$(pwd)"
echo project root set as "$SKYLIGHT_ROOT"


# remove existing database files
mkdir sms/database
cd sms/database
for i in master.db courses.db 2*
do
    echo removing old "$i"
    rm "$i"
done


# run the setup scripts
cd "$SKYLIGHT_ROOT"
pip3 install numpy==1.17.3 pandas==0.25.2
echo

for ex in \
    generate_models.py \
    personal_info.py \
    course_details.py \
    "generate_courses_and_credits.py" \
    "generate_course_reg_and_result.py" \
    generate_grading_rule.py \
    generate_categories.py \
    generate_degree_class.py
do
    echo running setup/src/$ex
    python3 setup/src/$ex
    echo
done

echo
ls -og sms/database/
echo
echo curr working dir: "$(pwd)"
