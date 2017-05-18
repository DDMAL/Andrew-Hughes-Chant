# Andrew-Hughes-Chant

# What are these files?

There are several files to address: 

(1) ```v2-CHNT.txt```: Andrew Hughes' original idiosyncratic notated Chant file – encoded by a special format;  

(2) ```Parser.py```: A script parsing the whole text file, extracting each song into a text file, and building the whole hierarchy readable file system which is indicated by the original text file (volumn, saint, service, etc.), at the same time, it generates ```.mei``` files with pitch.   

(3) ```Template.mei```: means they are used to generate ```.mei``` files using Pymei.  

(4) ```file_structure_text_file_MEI_file```: it contains the readable file structure, the original encodings for each chant, and ```.mei``` files with pitch, which is translated from the original encodings.

# How to use these files?
First clone the repository, if you just need all chants, just go into ```file_structure_text_file_MEI_file``` and you will find all the chants encoded in ```.mei``` files, which can be rendered by ```Verovio```, so you can view the score. 

If you want to generate these ```.mei``` files on your own, just run ```Parser.py``` and then the script will display some options for your to customize, then ```.mei``` files will be generated automatically.

In order to run ```Parser.py```, this is what you need to do:

# How to run Parser.py?
Note that you need Python3 ,cltk, and Pymei toolkit to run this script. You can install cltk toolkit simply by running: ``` pip3 install cltk```in the terminal.  

To install Pymei, please refer to: https://github.com/DDMAL/libmei/wiki.

First install libmei, then install the Python bindings.

# How is the chant encoded into MEI format?

There are cases where the mensual notations cannot be rendered, so some common music notation symbol is used:

(1) Plica is replaced by grace note, so when you see the score has a grace note, it actually indicates a plica.

(2) Ligature is represented as a slur.
