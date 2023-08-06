#!/bin/bash
# from Goldendoodle/goldendoodle: ./goldendoodle/doctest\&sphinx.sh > goldendoodle/reports/stdout.txt 2> goldendoodle/reports/stderr.txt

ABSOLUTE_DIRECTORY=$(dirname "$(realpath "${BASH_SOURCE:-$0}")")
NOW="$(date +"%Y-%m-%d %T")"

command () {
    # $1 := command; $2 := line no --> rc; $3 highest allowed rc
    line=$2
    allowedRc=$3
    $1
    rc=$?
    if [ $rc -gt $allowedRc ]; then
        echo "${NOW} $0 E command: $1 rc=$rc > allowed rc=$allowedRc"
        exit $line
    else
        echo "${NOW} $0 I command: $1 rc=$rc <= allowed rc=$allowedRc"
    fi 
}

command "cd ${ABSOLUTE_DIRECTORY}" $LINENO 0

command "poetry update" $LINENO 0

command "python -m doctest -o FAIL_FAST $(find . -type f -iname "*.py" -not -path "./docs/*")" $LINENO 0

command "sphinx-build -b html docs/source/ docs/build/" $LINENO 0
echo "Attention: sphinxs does not set rc after errors, so examine the output carefully."

command "xdg-open http://127.0.0.1:5500/goldendoodle/docs/build/index.html" $LINENO 0

command "echo 'end of script'" $LINENO 0