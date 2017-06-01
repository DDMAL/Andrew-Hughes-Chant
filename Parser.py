# -*- coding: utf-8 -*-
__author__ = "Yaolong Ju (yaolong.ju@mail.mcgill.ca)"
__date__ = "2017"
import os
import codecs
import sys
from cltk.stem.latin.syllabifier import Syllabifier
sys.path.append('/Users/yaolongju/Documents/Projects/libmei/python') #This is for Mac Mini
#sys.path.append('/Users/yaolong/Documents/Projects/libmei/python') #This is for the vm on Rescue
import pymei
import re


def add_each_meta_data(parent, elementname, content):
    """
    Add each meta-data to the header
    :param parent:
    :param element:
    :param content:
    :return:
    """
    element = pymei.MeiElement(elementname)
    element.setValue(content)
    parent.addChild(element)
    return parent


def add_meta_data(doc, mode=None, final=None, title=None, office=None, saint=None, feast=None, lyrics=None):
    """
    Add meta-data to MEI file.
    :param doc:
    :param mode:
    :param final:
    :param title:
    :param office:
    :param saint:
    :param feast:
    :param lyrics:
    :return:
    """
    if title != None :
        TITLES = doc.getElementsByName('title')
        TITLE = TITLES[0]
        TITLE.setValue(title) # add title
    TITLESTATEMENTS = doc.getElementsByName('fileDesc')
    TITLESTATEMENT = TITLESTATEMENTS[0]
    if mode != None :
        TITLESTATEMENT = add_each_meta_data(TITLESTATEMENT, 'mode', mode)
    if final != None :
        TITLESTATEMENT = add_each_meta_data(TITLESTATEMENT, 'final', final)
    if office != None:
        TITLESTATEMENT = add_each_meta_data(TITLESTATEMENT, 'office', office)
    if saint != None:
        TITLESTATEMENT = add_each_meta_data(TITLESTATEMENT, 'saint', saint)
    if feast != None:
        TITLESTATEMENT = add_each_meta_data(TITLESTATEMENT, 'feast', feast)
    if lyrics != None:
        TITLESTATEMENT = add_each_meta_data(TITLESTATEMENT, 'lyrics', lyrics)
    return doc


def print_measure(id, section):
    """
    A function that creates measure element under <section> hierarchy.
    :param id: Integer, the id of the measure.
    :param section: The pymei object of <section>
    :return:
    """
    measure = pymei.MeiElement('measure')
    staff = pymei.MeiElement('staff')
    layer = pymei.MeiElement('layer')
    section.addChild(measure)
    measure.addChild(staff)
    staff.addChild(layer)
    measure.addAttribute('n', '{}'.format(id))
    return layer


def add_note(pname, oct, layer, status, ptr, slur):
    """
    A function that creates notes element under <layer> hierarchy.
    :param pname: Char, pitch name
    :param oct: Int, octave of the note
    :param layer: The pymei object of <layer>, <note> is under it.
    :param status: Indicate whether the current note is connected with a slur or not.
    :param ptr: The id of note
    :return:
    """
    measure = layer.getAncestor('measure')
    if  pname == '?' :  # use <space> to indicate a blank spot
        note = pymei.MeiElement('space')
        note.setId(status + str(ptr))
        note.addAttribute('dur', '4')
        layer.addChild(note)
        dir = pymei.MeiElement('dir')
        dir.addAttribute('startid', '#' + status + str(ptr))
        dir.addAttribute('place', 'below')
        dir.setValue('?')  # use ? to indicate unknown pitch
        measure.addChild(dir)
    else:
        note = pymei.MeiElement('note')
        layer.addChild(note)
        note.addAttribute('pname', '{}'.format(pname))
        note.addAttribute('oct', '{}'.format(oct))
        note.addAttribute('dur', '4')
        note.addAttribute('stem.dir', 'up')
        note.addAttribute('stem.len', '0')
    #note.addAttribute('artic', 'acc')
    if status == 'i' :
        note.setId(status + str(ptr))
        slur = pymei.MeiElement('slur')
        slur.addAttribute('startid', '#' + status + str(ptr))
        slur.addAttribute('curvedir', 'above')
    elif(status == 'm'):
        note.setId(status + str(ptr))
    elif(status == 't'):
        note.setId(status + str(ptr))
        slur.addAttribute('endid', '#' + status + str(ptr))
        measure.addChild(slur)

    return note, slur


def add_grace_note(pname, oct, layer, status, ptr, slur):
    """
    A function that creates grace notes element under <layer> hierarchy.
    :param pname: Char, pitch name
    :param oct: Int, octave of the note
    :param layer: The pymei object of <layer>
    :param ptr: The id of note
    :param status: the status list
    :return:
        """

    measure = layer.getAncestor('measure')
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname', '{}'.format(pname))
    note.addAttribute('oct', '{}'.format(oct))
    note.addAttribute('dur', '8')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    note.addAttribute('grace', 'acc')
    if(status[ptr] == 'i'):  # slur needs to begin with the next note
        note.setId(status[ptr + 1] + str(ptr + 1))
        slur = pymei.MeiElement('slur')
        slur.addAttribute('startid', '#' + status[ptr + 1] + str(ptr + 1))
        slur.addAttribute('curvedir', 'above')
    elif(status == 'm'):
        note.setId(status + str(ptr))
    elif(status[ptr] == 't'):  # slur needs to begin with the previous note
        note.setId(status[ptr] + str(ptr))
        slur.addAttribute('endid', '#' + status[ptr - 1] + str(ptr - 1))
        measure.addChild(slur)
    return note, slur


def add_lyrics(note, syllable):
    """
    A function that creates 'verse' and 'syl' hierarchy under 'note' and adds lyrics
    under <syl> hierarchy.
    :param note: The note object of pymei.
    :param syllable: The syllable to add to MEI file.
    :return:
    """
    verse = pymei.MeiElement('verse')
    syl = pymei.MeiElement('syl')
    note.addChild(verse)
    verse.addAttribute('n', '1')
    syl.setValue(syllable)
    verse.addChild(syl)


def print_note(pitchid, octid, layer, ptr, status, syllable, ptr2, slur):
    """
    Add notes to MEI stream
    :param pitchid: Char, pitch.
    :param octid: Int, octave.
    :param layer: A hirarchical layer before <note>.
    :param ptr: The id of note
    :param status: The status of the note: is it just note, or note attached with lyrics, or grace note.
    :param syllable: The possible syllable attached to the note
    :param ptr2: The id  of the syllable
    :return:
    """

    if status[ptr] == 'n' or status[ptr] == 'i' or status[ptr] == 'm' or status[ptr] == 't':  # add note with slurs, or without slurs
        if len(status) - 1 > ptr:
            if status[ptr + 1] != 'g':
                note, slur = add_note(pitchid[ptr], octid[ptr], layer, status[ptr], ptr, slur)
                return 1, slur
            else:
                note, slur = add_grace_note(pitchid[ptr], octid[ptr], layer, status, ptr, slur)
                return 0, slur
        else:
            note, slur = add_note(pitchid[ptr], octid[ptr], layer, status[ptr], ptr, slur) # do not miss the last note!
            return 1, slur
    elif status[ptr] == 'l':  # syllable
        if (len(status) - 1 > ptr):
            note, slur = add_note(pitchid[ptr + 1], octid[ptr + 1], layer, status[ptr + 1], ptr, slur)
            add_lyrics(note, syllable[ptr2])
            return 1, slur
        else:
            note, slur = add_note(pitchid[ptr], octid[ptr], layer, status[ptr], ptr, slur) # do not miss the last note!
            add_lyrics(note, syllable[ptr2])
            return 1, slur
    return 0, slur


def num_to_pitch_class_with_oct(num, final, oct):
    """
    Transform number into pitch-class, which is key-sensitive.
    :param num: Int, the number which the original encoding uses.
    :param final: The tonic center.
    :param oct: The octave array.
    :return:
    """
    pitchclass = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    # mod = SearchMode(mode)
    for ptr in range(len(num)):
        for i in range(7):
            if final == pitchclass[i]:
                break
        if num[ptr] == '>':
            num = num[0:ptr] + '3' + num[ptr + 1:]
            oct[ptr] += 1
        elif num[ptr] == '-':
            num = num[0:ptr] + '6' + num[ptr + 1:]
            oct[ptr] -= 1
        elif num[ptr] == '0':
            num = num[0:ptr] + '7' + num[ptr + 1:]

            oct[ptr] -= 1
        elif num[ptr] == '*':
            num = num[0:ptr] + '5' + num[ptr + 1:]

            oct[ptr] -= 1
        elif num[ptr] == '%':
            num = num[0:ptr] + '4' + num[ptr + 1:]
            oct[ptr] -= 1
        elif num[ptr] == '=':
            num = num[0:ptr] + num[ptr - 1] + num[ptr + 1:]
            oct[ptr] = oct[ptr - 1]
        if num[ptr].isdigit():  # convert digit into pitch-class
            m = int(num[ptr])  # current digit
            ii = i
            for j in range(m - 1):
                i += 1
                ii += 1
                if ii >= 7:
                    oct[ptr] += 1
                    ii %= 7
                i %= 7
            num = num[0:ptr] + pitchclass[i] + num[ptr + 1:]
    return num, oct


def fill_in_status(melody, status, counterofsyl):
    """
    fill in the status list
    :param melody: the melody string
    :param status: the status list need to fill in to indicate whether it is a note, or a slur, etc.
    :param counterofsyl: the total number of syl
    :return: status, counterofsyl
    """
    for i, item in enumerate(status):
        if melody[i] == ',':
            status[i] = 'g'
        elif melody[i] == '.':
            status[i] = 'l'
            counterofsyl += 1
        elif melody[i] == '\'':
            status[i] = 's'  # ligature, represented by slur
        else:
            status[i] = 'n'
    return status, counterofsyl


def fill_in_slur_status(status):
    """
    Specify whether is the note at the beginning (i), middle (m), or end (t) of the slur
    :param melody: the melody string
    :param status: the status list need to fill in to indicate whether it is a note, or a slur, etc.
    :param counterofsyl: the total number of syl
    :return: status, counterofsyl
    """
    for i, item in enumerate(status):  # go over the status list again to specify which notes are connected with slurs
        if item == 's':
            j = i - 1  # see how many notes before slur (connected by a slur)
            while  status[j] == 'n' :
                j -= 1
            numofnoteswithslur = i - j - 1
            if  numofnoteswithslur == 1 :
                status[j + 1] = 'i'
            elif  numofnoteswithslur == 2 :
                status[j + 1] = 'i'
                status[j + 2] = 't'
            elif  numofnoteswithslur > 2 :
                status[j + 1] = 'i'
                status[i - 1] = 't'
                for k in range(j + 2, i - 1):
                    status[k] = 'm'
            j = i + 1 # see how many notes after slur
            while (status[j] == 'n'):
                    j += 1
                    if(j == len(status)):
                        break

            numofnoteswithslur = j - i - 1
            if  numofnoteswithslur == 1 :
                status[i + 1] = 'i'
            elif  numofnoteswithslur == 2 :
                status[i + 1] = 'i'
                status[i + 2] = 't'
            elif  numofnoteswithslur > 2 :
                status[i + 1] = 'i'
                status[j - 1] = 't'
                for k in range(i + 2, j - 1):
                    status[k] = 'm'

    return status


def melody_line_to_MEI_func(melody, input, syllable, faketitle, saint, office):
    """
    A conclusive function that uses several sub-functions to format MEI file, and add meta-data to MEI files, except for title.
    :param melody: The original melody line.
    :param input: Two chars that contain the modality and the tonic center.
    :param syllable: The string array to store the syllables.
    :return:
    """

    doc = pymei.documentFromFile(cwd + '/Template.mei').getMeiDocument()
    ptr = 0
    mode = input[0]
    final = input[1].lower()
    doc = add_meta_data(doc=doc, mode=mode, final=final, saint=saint, office=office)
    #if final not in 'abcdefg':
        #print("final not found")
        #input("??")
    counterofsyl = 0
    length = len(melody)
    pitchclass = [' ' for i in range(len(melody))]
    oct = [4 for i in range(len(melody))]
    status = [' ' for i in range(len(melody))] # 0 for grace note
    status, counterofsyl = fill_in_status(melody, status, counterofsyl)
    status = fill_in_slur_status(status)
    (melody, oct) = num_to_pitch_class_with_oct(melody, final, oct)
    i = 0
    measureptr = 0
    sections = doc.getElementsByName('section')
    section = sections[0]  # fill in from here
    slur = pymei.MeiElement('slur')
    while i < length:
        if measureptr % 4 == 0 and measureptr != 0 and increment != 0:
            layer = print_measure(measureptr / 4 + 1, section)
        elif measureptr % 4 == 0 and measureptr == 0:
            layer = print_measure(measureptr / 4 + 1, section)
        increment,slur = print_note(melody, oct, layer, i, status, syllable, ptr, slur)
        if status[i] == 'l':
            i += 1
            ptr += 1
        if i == length:  # it is possible that the last one of status is l
            break
        measureptr += increment
        i += 1
    return counterofsyl, doc


def regulate_name(matrix, line):
    """
    Regulate name and keep only the characters that exist in matrix
    :param matrix: Define characters to exist
    :return:
    """
    ascii = 128
    for i in range(ascii):
        ASCII = chr(i)
        if not ASCII in matrix:
            if not (ASCII.isalpha() or ASCII.isdigit()):
                line = line.replace(ASCII, '')
    return line


def is_non_vowel_syllable(syllable):
    """
    Exmaine whether this "syllable" really has a vowel or not.
    :param syllable:
    :return:
    """
    for i in syllable:
        if(i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u'):  # If a vowel is ever found, return False
            return False
    return True


def syllabifier_post_processing2(list):
    """
    Deal with exceptions
    :param list: the syllabified result that needs to correct
    :return:
    """
    for i, element in enumerate(list):
        if element == 'i' and (list[i - 1] == 'gu' or list[i - 1] == 'qu'):
            two_syllables_into_one(list, i-1)
            return list
        if (i < len(list) - 1):
            if list[i][-1] == 'i' and list[i + 1][0:2] == 'un':  # iun should be one syllable
                list[i] = list[i] + list[i + 1]
                del list[i + 1]
                return list
        else:
            if list[i - 1][-1] == 'i' and list[i][0:2] == 'un':  # iun should be one syllable
                input('iun at the end???')
                list[i - 1] = list[i - 1] + list[i]
                del list[i]
                return list



    return list

def two_syllables_into_one(list, i):
    """
    Combine two "syllables" into one
    :param list:
    :param i:
    :return:
    """
    if (i < len(list) - 1):
        list[i] = list[i] + list[i + 1]
        list.remove(list[i + 1])
        print(list)
        return list
    else:
        list[i - 1] = list[i - 1] + list[i]
        list.remove(list[i])
        print(list)
        return list
def syllabifier_post_processing(list):
    """
    Fix errors in the syllabifier and output the right syllabification results
    :param list: the syllabified result that needs to correct
    :return:
    """
    twovowel = ['ae', 'eu', 'ei', 'ii', 'oe', 'ui', 'io', 'oa', 'oi']
    for i, element in enumerate(list):
        element = element.lower()
        print(list)
        if(is_non_vowel_syllable(element)):  # this is not a syllable, need to be combined with the next one
            list = two_syllables_into_one(list, i)
            return list
        for vowel in twovowel:  # These cases should be two syllables, not one, for cases like "Reiixxx", only slice once
            #print(vowel)
            if vowel in element:
                ptr = element.find(vowel)
                tmp = list[i]
                list[i] = tmp[:ptr + 1]
                list.insert(i+1, tmp[ptr + 1:])
                print(list)
                return list
        if(i < len(list) - 1):
            print(list[i][-1], list[i+1][0])  # for debug
            if(list[i][-1] == 'e' and list[i + 1][0] == 'e') or (list[i][-1] == 'i' and list[i + 1][0] == 'e') or (list[i][-1] == 'u' and list[i + 1][0] == 'a') or (list[i][-1] == 'u' and list[i + 1][0] == 'o') or (list[i][-1] == 'u' and list[i + 1][0] == 'u'):
                print("found", list[i][-1], list[i + 1][0])
                list[i] = list[i] + list[i+1]
                del list[i+1]
                return list
        else:
            print(list[i - 1][-1], list[i][0])  # for debug
            if i != 0 :  # because if i is 0, i-1 is still 0!
                if (list[i - 1][-1] == 'e' and list[i][0] == 'e') or (list[i - 1][-1] == 'i' and list[i][0] == 'e') or (
                        list[i - 1][-1] == 'u' and list[i][0] == 'a') or (list[i - 1][-1] == 'u' and list[i][0] == 'o') or (
                        list[i - 1][-1] == 'u' and list[i][0] == 'u'):
                    print("found", list[i - 1][-1], list[i][0])
                    list[i - 1] = list[i - 1] + list[i]
                    del list[i]
                    return list

    return list


def change_song_title(doc, lastdir, faketitle, word, type, changedir, counter, flag):
    """
    This is a function that changes the file title which is indicated in the text file.
    Since a name is needed to create a file, the files is first created, then renamed with
    a right name, which can be found in the chant lyrics line. This function is used to change
    title of the last chant. Also, it closes the MEI file and then add title meta-data to that.
    :param lastdir: It is possible that last chant and current chant are in a different directory
    :param faketitle: The old file name.
    :param word: Lyrics line, where the new title is hidden
    :param type: The extension of the file
    :param changedir: bool value, if true, it means the directory has changed, so lastdir is used to
    find the chant and change the name. If false, use the current file path of os.
    :param counter: counts the number of the files which have the same names
    :param flag: indicates whether the file strcuture is created
    :return:
    """
    for i in range(10000):
        if word[i] == '':
            break
    length = i
    # print (length)
    lengthoftitle = 8
    if length <= lengthoftitle:
        finallength = length
    else:
        finallength = lengthoftitle
    for i in range(finallength):  # assume that the title is no longer than 10 words
        if word[i][-1].isupper():
            break
    realtitle = ''
    for j in range(0, i + 1):
        realtitle = realtitle + word[j] + '_'
    realtitle = realtitle.lower()
    realtitle = regulate_name('_', realtitle)
    add_meta_data(doc=doc, title=realtitle[0].upper() + realtitle[1:-1])
    if(type == '.mei'):
        if changedir is True:
            pymei.documentToFile(doc, os.path.join(lastdir, faketitle + '.mei'))  # save
        else:
            pymei.documentToFile(doc, faketitle + '.mei')
    if flag == 0: # no file structure
        if os.path.isfile(os.path.join(os.getcwd(), faketitle + type)):
            if os.path.isfile(os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type)) == False: # if the read title does not exist
                #print(os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type))
                os.rename(os.path.join(os.getcwd(), faketitle + type),
            os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type))  # 0 is a space
            else:
                os.rename(os.path.join(os.getcwd(), faketitle + type),
                          os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + '_' + str(counter) + type))  # 0 is a space, if the
                counter += 1
    else: # file structure is created
        if changedir is True:  # change file name
            if os.path.isfile(os.path.join(lastdir, faketitle + type)):
                if os.path.isfile(os.path.join(lastdir, realtitle[0].upper() + realtitle[1:-1] + type)) == False:
                    os.rename(os.path.join(lastdir, faketitle + type),
                          os.path.join(lastdir, realtitle[0].upper() + realtitle[1:-1] + type))
                else:
                    os.rename(os.path.join(lastdir, faketitle + type),
                              os.path.join(lastdir, realtitle[0].upper() + realtitle[1:-1] + '_' + str(counter) + type))
                    counter += 1
        else:
            if os.path.isfile(os.path.join(os.getcwd(), faketitle + type)):
                if os.path.isfile(os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type)) == False:
                    os.rename(os.path.join(os.getcwd(), faketitle + type),
                          os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type))  # 0 is a space
                else:
                    os.rename(os.path.join(os.getcwd(), faketitle + type),
                              os.path.join(os.getcwd(),
                                           realtitle[0].upper() + realtitle[1:-1] + '_' + str(counter) + type))
                    counter += 1
    return counter, doc


def chunk_lyrics(lyrics, word, list):
    """
    This function chunked the lyrics into syllables using a syllabifier from cltk toolkit
    :param lyrics: A string. The original lyrics line
    :param word: Array for strings. each stores a word from the lyrics
    :param list: Array for strings, each stores a syllable
    :return:
    """
    # lyrics = lyrics.lower()
    vowel = ['a', 'e', 'i', 'o', 'u']
    coounter = 0
    sign = 0
    numofsyllable = 0
    numofword = 0
    sumnumofsyl = 0
    begin = end = 0
    for i, char in enumerate(lyrics):
        if char == ' ':
            if begin != end:  # not the first space
                end = i - 1
                word[numofword] = lyrics[begin:end + 1]
                numofword += 1
                begin = i + 1
            else:
                begin = 1  # skip the first space
    for i in range(numofword):
        # print (word[i])
        numofsyllable = 0
        tmp = syllabifier.syllabify(word[i].lower())

        for element in tmp:
            list[sumnumofsyl] = element
            numofsyllable += 1
            sumnumofsyl += 1
        numOfArtiSyl[i] = numofsyllable
    return sumnumofsyl


def generate_file_structure(line, ptr1, ptr2):
    """
    Generate the hierarchical folders, and return that name.
    :param line: The current line which contained the desired name of the folder
    :param ptr1: The pointer which points the beginning of the file name
    :param ptr2: The pointer which points the end of the file name
    :return:
    """
    folder_name = line[ptr1:ptr2]
    folder_name = regulate_name('_.=()-', folder_name) # Make sure that the file name is compatible with Windows
    if os.path.exists(folder_name) is False:
        # The name of directory can not have space!
        if(len(folder_name) < 1):
            folder_name = 'NO_NAME'
            os.mkdir(folder_name)  # In this case, the name of the folder is empty!
        else:
            os.mkdir(folder_name)  # create the folder for each volume
    os.chdir(folder_name)  # go into that folder
    return line[ptr1:ptr2]


def parse(filex, flag1, flag2, flag3):
    """
    The function that parses the original file with Hughes' encodings.
    :param filex: The file pointer that points to the original file
    :param flag1: Whether to generate the file structure
    :param flag2: Whether to generate the text file
    :param flag3: Whether to generate the MEI file
    :return:
    """
    syllable = [' ' for i in range(10000)]
    word = [' ' for i in range(10000)]
    numOfRealSyl = [0 for i in range(10000)]
    counter = 0
    numOfSameFileName = 0

    melodyLine = ['%', '*', '-', '>', '.', '\'', '=', ',',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '?']  # char we need from melody line
    cwd = os.getcwd()
    ChangeDir = False
    log = open('SyllabifierLog.txt', 'w')
    endOfMelodySign = False
    endOfLyricsSign = False  # There will be exceptions where the line is not complete within a line
    print(filex)
    mark = 0  # not find a head yet
    f1 = open(filex, 'r', encoding='cp437')  # the actual encoding is cp437, not iso8859!
    line = f1.readline()
    if (flag1 == 0):
        if os.path.exists("text_file") is False:
            os.mkdir('text_file')
        os.chdir('text_file')
    while line:
        line = line.replace('«', '<<')
        line = line.replace('»', '>>')
        if (line.find('[File') != -1 or line.find('[file') != -1) and (mark == 0 or mark == 4):
            print(line)  # show all the volumes
            line = line.replace(' ', '')  # The name of directory can not have space!
            ptr = line.find('CH-')
            print(line[ptr:ptr + 4])
            if (mark == 4):  # this means changing dir from chant from last vol to a new vol
                LastDir = os.getcwd()
                ChangeDir = True
                if(flag1 == 1):
                    os.chdir(os.pardir)
                    os.chdir(os.pardir)
                    os.chdir(os.pardir)
                    os.chdir(os.pardir)
            if os.path.exists(line[ptr:-2]) is False:
                if line.find('MDNM') != -1:  # MDNM is not wanted
                    ptr3 = line.find('MDNM')
                    if(flag1 == 1):
                        generate_file_structure(line, ptr, ptr3 - 2)
                else:
                    if (flag1 == 1):
                        generate_file_structure(line, ptr, -2)
            mark = 1  # write volumn file
            # continue # read next line
        elif (line.find(
                '|.') == -1 and mark == 1):  # Not saint yet, it will be head instructions, save it into file
            if flag1 == 1 and flag2 == 1:
                fI = codecs.open('VolumnHeader.txt', 'a+', 'utf-8')
                fI.write(line)
        elif ((mark == 1 or mark == 4) and (
                            line.find('=') == -1 or line.find('70=XCX') != -1 or line.find('8=0504') != -1 or (
                            line.find('(') != -1 and line.find(')') != -1) or line.find('[Advent') != -1) and line.find(
            '|.') != -1):  # find a saint, continue to create folder for that saint
            # print (line)
            if flag1 == 1 and flag2 == 1:
                fI.close()
            line = line.replace(' ', '_')  # The name of directory can not have space!
            line = line.replace('\t', '-')
            line = line.replace('"', '-')

            if line.find('X_') or line.find('K_') != -1:
                if (mark == 4):
                    LastDir = os.getcwd()
                    ChangeDir = True
                    if (flag1 == 1):
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                if line.find('X_') != -1:  # try to find the name of the saint
                    ptr = line.find('X_') + 2
                elif line.find('K_') != -1:  # try to find the name of the saint
                    ptr = line.find('K_') + 2
                if line.find(')') != -1:
                    ptr4 = line.find(')')  # only keep the saint's name
                    if (flag1 == 1):
                        saint = generate_file_structure(line, ptr, ptr4)  # real saint's name
                else:
                    if (flag1 == 1):
                        saint = generate_file_structure(line, ptr, -1)  # real saint's name
                if line.find('|.') != -1:
                    ptr2 = line.find('|.')
                    if line.find('_(') != -1:
                        ptr3 = line.find('_(')
                        if (flag1 == 1):
                            generate_file_structure(line, ptr2 + 2, ptr3)  # original file name, invalid!
                    else:
                        if (flag1 == 1):
                            generate_file_structure(line, ptr2 + 2, ptr - 2)  # original file name, invalid!
                else:  # always deal with exception
                    if (flag1 == 1):
                        saint = generate_file_structure(line, 0, ptr - 2)  # never happened actually
            else:  # if there is an exception, do as usual
                ptr = line.find('|.')
                if (mark == 4):
                    LastDir = os.getcwd()
                    ChangeDir = True
                    if (flag1 == 1):
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        saint = generate_file_structure(line, ptr + 2, -2)  # never happened actually
            mark = 2  # write saint file
            # continue
        elif mark == 2 and line.find('|.') == -1:
            if flag1 == 1 and flag2 == 1:
                fI = codecs.open('SaintHeader.txt', 'a+', 'utf-8')
            # print (line)
                print(line, file=fI)
        elif (mark == 2 or mark == 4) and line.find('=') != -1 and line.find('|.') != -1:  # saint's name=letter
            print(line)
            if flag1 == 1 and flag2 == 1:
                fI.close()
            line = line.replace('"', '-')
            line = line.replace('?', '-')
            line = line.replace('/', '-')
            line = line.replace(' ', '')
            line = line.replace('=L', '=Lauds')
            line = line.replace('=M', '=Matins')
            line = line.replace('=V', '=Vespers')
            line = line.replace('=W', '=2nd_Vespers')
            ptr = line.find('=')  # remove redundant file name, like 'AD00'
            #ptr = line.find('|.')
            if (mark == 4):
                LastDir = os.getcwd()
                ChangeDir = True
                if (flag1 == 1):
                    os.chdir(os.pardir)
            if line.find('<<MDNM') != -1:
                ptr2 = line.find('<<MDNM')
                if (flag1 == 1):
                    office = generate_file_structure(line, ptr + 1, ptr2)
            else:  # always deal with exception
                if (flag1 == 1):
                    office = generate_file_structure(line, ptr + 1, -2)
            mark = 3  # write saint= letter head file
            # continue
        elif mark == 3 and line.find('|g') == -1:
            if flag1 == 1 and flag2 == 1:
                fI = codecs.open('__LetterHeader.txt', 'a+', 'utf-8')
                print(line)
                fI.write(line)
                #if(line!='\n'):
                    #print('it is not blank all the time')
        elif (mark == 3 or mark == 4) and line.find('|g') != -1 and line.find('=') != -1 and line.find('.') != -1:
            if line.find('|g') != -1:  # find the individual song
                # if(counter != 0): fmei.close()
                filename = line  # reserve the original file name
                if filename.find('|g343 =MV10.8v') != -1:
                    print(filename)
                line = line.replace(' ', '')
                ptr2 = line.find('.')
                mode = line[ptr2 + 1:ptr2 + 3]  # get the mode and tonal center
                print(mode)
                ptr = line.find('|g')
                line = line.replace('?', '-')
                line = line.replace('/', '-')
                counter += 1  # num of songs
                print (counter)
                print ()
                signWriteToMei = False  # have not wrote to file
                tmpTitle = line[ptr + 1:-2]
                print(tmpTitle)
                if tmpTitle.find('(') != -1:  # exception: the title can append a very long message within ()
                    ptr3 = tmpTitle.find('(')
                    tmpTitle = tmpTitle[0:ptr3] + tmpTitle[-2:-1]
                    # trick, since if the information within () is cut off, some file name will be the same,
                    # and it will cause prob
                if flag2 == 1:
                    fsong = codecs.open(tmpTitle + '.txt', 'a+', 'utf-8')
                endOfLyricsSign = False
                endOfMelodySign = False  # Update the sign, since it is a new song!
                # fmei=codecs.open(line[ptr+1:-2]+'.mei','a+','utf-8')
                if counter != 1:  # change the title of the last song
                    # change_song_title(LastDir, FakeTitle, word, '.mei', ChangeDir)
                    if flag2 == 1:
                        numOfSameFileName, doc = change_song_title(doc, LastDir, FakeTitle, word, '.txt', ChangeDir,
                                                              numOfSameFileName, flag1)
                    if flag3 == 1:
                        numOfSameFileName, doc = change_song_title(doc, LastDir, FakeTitle, word, '.mei', ChangeDir,
                                                              numOfSameFileName, flag1)
                    ChangeDir = False  # only deal with the last file in the last dir
                FakeTitle = tmpTitle
                # print (line)
                if flag2 == 1:
                    print(line, file=fsong, end='')
                # print(line, file=log)
                mark = 4  # write individual song
                # continue
        elif (line.find('|.') == -1 and line.find('[File') == -1 and line.find('[file') == -1 and line.find(
                '|g') == -1 and mark == 4):  # write lines into a txt file
            # print (line)
            #  Since some words will be missing in the lyrics line, we have to extract lyrics from this line
            if (os.getcwd().find('CH-C') != -1):
                print('debug')
            signWriteToMei = True  # After writing this line, write to mei file
            line = re.sub(r'\(!\d\)', '', line)  # need to use '\' to match '()' to replace (!1) exception
            if(flag2 == 1):
                print(line, file=fsong, end='')
            if line[0:2] == '\ ' or line[2:4] == '\ ':  # this is melody with lyric line
                print(line)
                if line.find('\()')!= -1 or line.find('\ ()') != -1:  # This ensures that the melody line is finished
                    endOfMelodySign = True
                while line.find('\()') == -1 and endOfMelodySign is False:  # nasty exceptions
                    newline = f1.readline()
                    print(newline, file=fsong)
                    line += newline  # read new line and append to the original until the end
                if line.find('\()') == -1 and endOfMelodySign == True:  # exceptions!
                    print("error")  # There are occasions where there is more than one
                        # melody lines,
                    if line.find('\(ve)') != -1:  # deal with exceptions case by case
                        line = f1.readline()  # discard this line, since it is not a melody line
                        continue
                    if line.find('(v in Sarum) ??') != -1:
                        line = f1.readline()  # discard this line, since it is not a melody line
                        continue
                    if line.find('et.21,=0') != -1:
                        line = f1.readline()  # discard this line, since it is not a melody line
                        continue
                ascii = 128
                for i in range(ascii):
                    ASCII = chr(i)
                    if not ASCII in melodyLine:
                        if not ASCII.isalpha():
                            line = line.replace(ASCII, '')
                line = line.replace('  ', ' ')
                lyricsLine = line
                for i in lyricsLine:
                    if not i.isalpha():
                        if(i == ' '):
                            continue  # skip space
                        lyricsLine = lyricsLine.replace(i,'')
                lyricsLine = lyricsLine.replace('  ', ' ')
                lyricsLine = lyricsLine.replace('  ', ' ')
                print(lyricsLine)
                if lyricsLine == lyricsLine2 :
                    syllabifierNum = chunk_lyrics(lyricsLine2, word, syllable)  # ptrBegin is not used, since the fuction need the space for the begin and the end to work properly
                else:
                    syllabifierNum = chunk_lyrics(lyricsLine, word, syllable)
                for i in range(len(line)):
                    if not line[i] in melodyLine:
                        if not line[i].isalpha():
                            print('ERROR')
                            print(line[i])  # for debug
                # count the syllables for each word
                numOfDot = 0
                numofword = 0
                for i in range(1, len(line)):
                    if line[i] == '.':
                        numOfDot += 1
                    elif line[i] == ' ' and numOfDot!= 0:  # last word ends, new word begins, and the numOfDot should
                        # be non-zero, since there are exceptions! (Syllabifier and Hughes' results mismatch)
                        numOfRealSyl[numofword] = numOfDot
                        numofword += 1
                        numOfDot = 0
                        # end
                for i in range(len(line)):
                    if line[i].isalpha():
                        line = line.replace(line[i], ' ')
                line = line.replace(' ', '')
                print(('melody' + line))  # debug
                (realSyllableNum, doc) = melody_line_to_MEI_func(line, mode,
                                                                 syllable, FakeTitle, saint, office)  # line2 = line.replace('.', '')  # melody with syllable sign
                if realSyllableNum != syllabifierNum:
                    flag4 = 0
                    counter2 = 0  # calculate the number of syllables produced by the Syllabifier
                    for i in range(numofword):
                        if numOfRealSyl[i] != numOfArtiSyl[i]:  # only output different ones
                            syllables = syllabifier.syllabify(word[i])
                            syllables = syllabifier_post_processing(syllables)  # only post-process it when they do not agree!
                            syllables = syllabifier_post_processing2(syllables)
                            for j in range(counter2, counter2 + numOfArtiSyl[i]):
                                del syllable[counter2]
                            for j in range(counter2, counter2 + len(syllables)):
                                syllable.insert(j, syllables[j - counter2])
                            if(len(syllables) != numOfRealSyl[i]):  # real discrepancies
                                if(flag4 == 0):
                                    print('---------------------------------------', file=log)
                                    print(filename + os.getcwd(), file=log)

                                    print("Total num of syllables from Hughes    : ", realSyllableNum, file=log)
                                    print("Total num of syllables from Syllabifier: ", syllabifierNum, file=log)
                                    flag4 = 1
                                print(word[i], file=log)
                                print(numOfRealSyl[i], "syllables from Hughes' encoding", file=log)
                                print(numOfArtiSyl[i], "syllables from the Syllabifier:", syllables,
                                      file=log)
                            # str = input("What do you think about it?")
                            # print(str)
                            # line = line.replace(',', '')
                            counter2 += len(syllables)
                        else:
                            counter2 += numOfArtiSyl[i]
            elif line[0:2] == '/ ' or line[2:4] == '/ ':  # lyric line
                pointer = line.find('/ ')  # for exception: some lines begins with space than '/ '
                #if line.find('excelsuS') != -1:  # for debug
                    #print('debug')
                if line.find('pio festo') != -1:
                    print('continue')
                if line[-4:-1] == '/()':  # this does not have exceptions so far
                    endOfLyricsSign = True  # It means the lyrics are complete
                while line.find('/()') == -1 and endOfLyricsSign is False:  # nasty exceptions
                    if(line.find(' /\n') != -1 and filename.find('(h CAO 1873)') == -1 and filename.find('(h CAO 2593)') == -1
                       and filename.find('(h CAO 1924)') == -1 and filename.find('(h CAO 2619)') == -1 and filename.find('|g29 =VE.6f') == -1
                       and filename.find('|g162 =MR5.1d') == -1 and filename.find('|g221 =MA9.8g') == -1):
                        # exclude these files, since the melody ends with '/', not '/()', exceptions! These cases both contain ' /' and '/()', need to exclude as well.
                        print('desired result?')  # to find these cases in the debug mode, and can document it if needed
                        break
                    else:
                        newline = f1.readline()
                        if(flag2 == 1):
                            print(newline, file=fsong)
                        line += newline
                if line.find('luminI.1.1.1;') != -1:  # exception where his encoding is wrong
                    print("unsolved exception")
                if line.find('/()') == -1 and endOfLyricsSign is True:  # Non-lyric line
                    print("ERROR!")
                else:
                    for i in line:
                        if(i == '+'):  # '+' cannot be replaced by a space!
                            line = line.replace(i, '')
                        elif (i.isalpha() or i == ' ') is False:
                            line = line.replace(i,
                                                ' ')  # replace anything other than letter or space into a space
                            # print(("lyric" + line))
                    while(line.find('  ') != -1):
                        line = line.replace('  ', ' ')  # multiple space is reduced to one
                lyricsLine2 = line
        line = f1.readline()

if __name__ == "__main__":
    cwd = os.getcwd()
    numOfArtiSyl = [0 for i in range(10000)]
    syllabifier = Syllabifier()
    for filex in os.listdir('.'):
        """
        Main function, where the whole file hirarchy is built and the '.txt' and '.mei' files are
        generated.
        """
        if os.path.isfile(filex) and (os.path.splitext(filex)[1][1:].lower() in 'txt') and (filex.find('v2-CHNT') != -1) is True:
            print(filex)
            print("Pasring the file, please specify the function you want, 1 means yes; 0 means no")
            flag1 = int(input("Generate file structure?"))
            flag2 = int(input("Generate text files?"))
            flag3 = int(input("Generate MEI structure?"))
            #flag1 = 1
            #flag2 = 1
            #flag3 = 1
            parse(filex, flag1, flag2, flag3)