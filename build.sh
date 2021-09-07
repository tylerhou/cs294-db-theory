#!/bin/sh

set -e

latexmk -pdf -pdflatex="pdflatex -halt-on-error -file-line-error -shell-escape %O %S" $1;

