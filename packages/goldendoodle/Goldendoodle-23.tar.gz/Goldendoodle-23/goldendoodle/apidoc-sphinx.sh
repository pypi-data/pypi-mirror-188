#!/bin/bash
# run from Goldendoodle/goldendoodle: ./apidoc-sphinx.sh

sphinx-apidoc -o docs/source_from-sphinx-apidoc -d 2 -e --implicit-namespaces -a -H 'Goldendoodle' -A 'Melchior im Dreital' -V '22.08' goldendoodle/goldendoodle/