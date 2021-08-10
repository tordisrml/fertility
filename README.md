# Hello
This is a git repository for the evolution and testing of a new breeding evaluation for fertility in Icelandic Dairy cattle.
Programs are written in Python

# Programs created:

## dmufertility.py
### This is the main program
Program that takes two data files from Huppa and creates a file to be used in DMU5 for fertility breeding evaluation.
Merges files, creates new fertility traits, creates fixed effects and
cleans data before evaluation.

# Extra programs created in alphabetical order:

## bassitdm.py
This program reads the bassitdm file from the current breeding evaluation
and currently writes to a new file the fertility results

## bull_checks.py
Checks how many daughters bulls have in the pedigree file.
Writes out a new file with bulls that have a certain amount of daughers.

## count_noparents.py
This program reads the pedigree file and counts the number of ghost parents

## dmufertility_CI
Creates a file for the evaluation of calving interval for DMU5 runs

## pedigree.py
Program that takes the pedigree file from Huppa and creates a pedigree file to be used in DMU5.
(...also created code IDs for DMU runs)

## samanburdur.py
Compares new fertility evaluation to old fertility evaluation
All animals from pedigree included

## samanburdur_bulls.py
Compares new fertility evaluation to old fertility evaluation
Only bulls that have more than 50+ daughters are included

## samanburdur_ownobss.py
Compares new fertility evaluation to old fertility evaluation
Only animals that have their own observation in the new fertility evaluation
are included

## sameining.py
This program combines new results from other sameining programs and old results
into one Datafile

## sameining_CI.py
This program reads the DMU5 calving interval SOL file and collects results into
a new file

## sameining_inbreed.py
This program reads the DMU5 7 trait inbreeding SOL file and collects results
into a new file.

## sameining_phantom.py
This program reads the DMU5 7 trait phantom group SOL file and collects results
into a new file.
