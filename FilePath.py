# -*- coding: utf-8 -*-
import os
import codecs
from cltk.stem.latin.syllabifier import Syllabifier
import sys
sys.path.append('/Users/yaolong/Documents/Projects/libmeiOldVersion/libmei/python')  # otherwise it can not be found!
import pymei


def change_song_title(lastdir, faketitle, word, type, changedir):
    """
    This is a function that changes the file title which is indicated in the text file.
    Since a name is needed to create a file, the files is first created, then renamed with
    a right name, which can be found in the chant lyrics line. This function is used to change
    title of the last chant.
    :param lastdir: It is possible that last chant and current chant are in a different directory
    :param faketitle: The old file name.
    :param word: Lyrics line, where the new title is hidden
    :param type: The extension of the file
    :param changedir: bool value, if true, it means the directory has changed, so lastdir is used to
    find the chant and change the name. If false, use the current file path of os.
    :return:
    """

    for i in range(10000):
        if word[i] == '':
            break
    length = i
    # print (length)
    lengthoftitle = 5
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
    if changedir is True:  # change file name
        if os.path.isfile(os.path.join(lastdir, faketitle + type)):
            os.rename(os.path.join(lastdir, faketitle + type),
                      os.path.join(lastdir, realtitle[0].upper() + realtitle[1:-1] + type))
    else:
        if os.path.isfile(os.path.join(os.getcwd(), faketitle + type)):
            os.rename(os.path.join(os.getcwd(), faketitle + type),
                      os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type))  # 0 is a space


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


def add_note(pname, oct, layer):
    """
    A function that creates notes element under <layer> hierarchy.
    :param pname: Char, pitch name
    :param oct: Int, octave of the note
    :param layer: The pymei object of <layer>, <note> is under it.
    :return:
    """
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname', '{}'.format(pname))
    note.addAttribute('oct', '{}'.format(oct))
    note.addAttribute('dur', '4')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    return note


def add_grace_note(pname, oct, layer):
    """
    A function that creates grace notes element under <layer> hierarchy.
    :param pname: Char, pitch name
    :param oct: Int, octave of the note
    :param layer: The pymei object of <layer>
    :return:
        """
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname', '{}'.format(pname))
    note.addAttribute('oct', '{}'.format(oct))
    note.addAttribute('dur', '8')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    note.addAttribute('grace', 'acc')
    return note


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


def add_lyrics2(note, syllable):
    """
    Another function to add lyrics on note level, which does not work, though.
    """
    note.addAttribute('syl', '{}'.format(syllable))


def print_note(pitchid, octid, layer, ptr, status, syllable, ptr2):
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
    if status[ptr] == 'n':
        if len(status) - 1 > ptr:
            if status[ptr + 1] != 'g':
                add_note(pitchid[ptr], octid[ptr], layer)
    elif status[ptr] == 'g':  # grace note
        add_grace_note(pitchid[ptr - 1], octid[ptr - 1], layer)
    elif status[ptr] == 'l':  # syllable
        if len(status) - 1 > ptr:
            note = add_note(pitchid[ptr + 1], octid[ptr + 1], layer)
            # add_lyrics(note, syllable[ptr2])
        '''elif(status[ptr]=='s'):
             tmpPtr = ptr-1
             while(status[tmpPtr]=='n'):
                 tmpPtr = tmpPtr - 1
             tmpPtr = tmpPtr + 1
             noteNum = ptr - tmpPtr # get the number of notes in with a slur
             startSlur = measurePtr - noteNum
             endSlur = measurePtr
             newFid.write("< slur tstamp = \"%i\" tstamp2 = \"0m+%i\" curvedir = \"above\" / >\n"  % (measurePtr%4+1, noteNum))'''


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
    for ptr, char in enumerate(num):
        for i in range(7):
            if final == pitchclass[i]:
                break
        if char == '>':
            num = num[0:ptr] + '3' + num[ptr + 1:]
            oct[ptr] += 1
        elif char == '-':
            num = num[0:ptr] + '6' + num[ptr + 1:]
            oct[ptr] -= 1
        elif char == '0':
            num = num[0:ptr] + '7' + num[ptr + 1:]

            oct[ptr] -= 1
        elif char == '*':
            num = num[0:ptr] + '5' + num[ptr + 1:]

            oct[ptr] -= 1
        elif char == '%':
            num = num[0:ptr] + '4' + num[ptr + 1:]
            oct[ptr] -= 1
        elif char == '=':
            num = num[0:ptr] + num[ptr - 1] + num[ptr + 1:]
            oct[ptr] = oct[ptr - 1]
        if char.isdigit():  # convert digit into pitch-class
            m = int(char)  # current digit
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


def melody_line_to_MEI_func(melody, input, syllable):
    """
    A conclusive function that uses several sub-functions to format MEI file.
    :param melody: The original melody line.
    :param input: Two chars that contain the modality and the tonic center.
    :param syllable: The string array to store the syllables.
    :return:
    """
    doc = pymei.documentFromFile(cwd + '/Template.mei').getMeiDocument()
    ptr = 0
    mode = input[0]
    final = input[1]
    counterofsyl = 0
    length = len(melody)
    pitchclass = [' ' for i in range(len(melody))]
    oct = [4 for i in range(len(melody))]
    status = [' ' for i in range(len(melody))]  # 0 for grace note
    for i in range(length):  # label each char in the string a specific function
        if melody[i] == ',':
            status[i] = 'g'  # g stands for grace note
        elif melody[i] == '.':
            status[i] = 'l'  # l stands for lyrics
            counterofsyl += 1
        elif melody[i] == '\'':
            status[i] = 's'  # ligature, represented by slur
        else:
            status[i] = 'n'  # n stands for note
    (melody, oct) = num_to_pitch_class_with_oct(melody, final, oct)
    i = 0
    measureptr = 0
    sections = doc.getElementsByName('section')
    section = sections[0]  # fill in from here
    while i < length:
        if measureptr % 4 == 0 and measureptr != 0:
            layer = print_measure(measureptr / 4 + 1, section)
        elif measureptr % 4 == 0:
            layer = print_measure(measureptr / 4 + 1, section)
        print_note(melody, oct, layer, i, status, syllable, ptr)
        if status[i] == 'l':
            i += 1
            ptr += 1
        if i == length:  # it is possible that the last one of status is l
            break
        if status[i] == 'n':
            if i < length - 1:
                if status[i + 1] != 'g':
                    measureptr += 1
        i += 1
    pymei.documentToFile(doc, FakeTitle + '.mei')
    return counterofsyl, doc


if __name__ == "__main__":

    format = ['txt']
    counter = 0
    syllable = [' ' for i in range(10000)]
    word = [' ' for i in range(10000)]
    numOfRealSyl = [0 for i in range(10000)]
    numOfArtiSyl = [0 for i in range(10000)]
    melodyLine = ['%', '*', '-', '>', '.', '\'', '=', ',',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']  # char we need from melody line
    cwd = os.getcwd()
    ChangeDir = False
    syllabifier = Syllabifier()
    # log = open('SyllabifierLog.txt', 'w')
    # globalSign = False  # for debug
    endOfMelodySign = False
    endOfLyricsSign = False  # There will be exceptions where the line is not complete within a line

    for filex in os.listdir('.'):
        """
        Main function, where the whole file hirarchy is built and the '.txt' and '.mei' files are
        generated.
        """
        if os.path.isfile(filex) and (os.path.splitext(filex)[1][1:].lower() in format) is True:
            print(filex)
            mark = 0  # not find a head yet
            f1 = open(filex, 'r', encoding='cp437')  # the actual encoding is cp437, not iso8859!
            line = f1.readline()
            while line:
                line = line.replace('«', '<<')
                if (line.find('[File') != -1 or line.find('[file') != -1) and (mark == 0 or mark == 4):
                    print(line)  # show all the volumes
                    line = line.replace(' ', '')  # The name of directory can not have space!
                    ptr = line.find('CH-')
                    print(line[ptr:ptr + 4])
                    if(mark == 4):  # this means changing dir from chant from last vol to a new vol
                        LastDir = os.getcwd()
                        ChangeDir = True
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                    if os.path.exists(line[ptr:-2]) is False:
                        if line.find('MDNM') != -1:  # MDNM is not wanted
                            ptr3 = line.find('MDNM')
                            os.mkdir(line[ptr:ptr3 - 2])  # remove MDNM staff
                            os.chdir(line[ptr:ptr3 - 2])
                        else:
                            os.mkdir(line[ptr:-2])  # create the folder for each volume
                            os.chdir(line[ptr:-2])  # go into that folder
                    mark = 1  # write volumn file
                    # continue # read next line
                elif (line.find(
                        '|.') == -1 and mark == 1):  # Not saint yet, it will be head instructions, save it into file
                    fI = codecs.open('VolumnHeader.txt', 'a+', 'utf-8')
                    fI.write(line)
                elif ((mark == 1 or mark == 4) and (line.find('=') == -1 or line.find('70=XCX') != -1 or line.find('8=0504') != -1 or (
                        line.find('(') != -1 and line.find(')') != -1) or line.find('[Advent') != -1) and line.find(
                        '|.') != -1):  # find a saint, continue to create folder for that saint
                    # print (line)
                    fI.close()
                    line = line.replace(' ', '_')  # The name of directory can not have space!
                    line = line.replace('\t', '-')
                    line = line.replace('"', '-')
                    if line.find('X_') or line.find('K_') != -1:
                        if(mark == 4):
                            LastDir = os.getcwd()
                            ChangeDir = True
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                        if line.find('X_') != -1:  # try to find the name of the saint
                            ptr = line.find('X_') + 2
                        elif line.find('K_') != -1:  # try to find the name of the saint
                            ptr = line.find('K_') + 2
                        if line.find(')') != -1:
                            ptr4 = line.find(')')  # only keep the saint's name
                            if os.path.exists(line[ptr:ptr4]) is False:  # create the folder of the saint s name
                                os.mkdir(line[ptr:ptr4])
                            os.chdir(line[ptr:ptr4])
                        else:
                            if os.path.exists(line[ptr:-1]) is False:  # create the folder of the saint s name
                                os.mkdir(line[ptr:-1])
                            os.chdir(line[ptr:-1])
                        if line.find('|.') != -1:
                            ptr2 = line.find('|.')
                            if line.find('_(') != -1:
                                ptr3 = line.find('_(')
                                if (os.path.exists(
                                        line[ptr2 + 2:ptr3]) is False):  # ptr3 means only keep ANNA like file name
                                    os.mkdir(line[ptr2 + 2:ptr3])  # then create the ID number of that saint
                                os.chdir(line[ptr2 + 2:ptr3])
                            else:
                                if (os.path.exists(
                                        line[ptr2 + 2:ptr - 2]) is False):  # ptr3 means only keep ANNA like file name
                                    os.mkdir(line[ptr2 + 2:ptr - 2])  # then create the ID number of that saint
                                os.chdir(line[ptr2 + 2:ptr - 2])
                        else:  # always deal with exception
                            if os.path.exists(line[:ptr - 2]) is False:
                                os.mkdir(line[:ptr - 2])  # then create the ID number of that saint
                            os.chdir(line[:ptr - 2])
                    else:  # if there is an exception, do as usual
                        ptr = line.find('|.')
                        if(mark == 4):
                            LastDir = os.getcwd()
                            ChangeDir = True
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                        if os.path.exists(line[ptr + 2:-2]) is False:
                            os.mkdir(line[ptr + 2:-2])
                        os.chdir(line[ptr + 2:-2])
                    mark = 2  # write saint file
                    # continue
                elif mark == 2 and line.find('|.') == -1:
                    fI = codecs.open('SaintHeader.txt', 'a+', 'utf-8')
                    # print (line)
                    print(line, file=fI)
                elif (mark == 2 or mark == 4) and line.find('=') != -1 and line.find('|.') != -1:  # saint's name=letter
                    print(line)
                    fI.close()
                    line = line.replace('"', '-')
                    line = line.replace('?', '-')
                    line = line.replace('/', '-')
                    line = line.replace(' ', '')
                    line = line.replace('=L', '=Lauds')
                    line = line.replace('=M', '=Matins')
                    line = line.replace('=V', '=Vespers')
                    line = line.replace('=W', '=2nd_Vespers')
                    ptr = line.find('|.')
                    if(mark == 4):
                        LastDir = os.getcwd()
                        ChangeDir = True
                        os.chdir(os.pardir)
                    if line.find('<<MDNM') != -1:
                        ptr2 = line.find('<<MDNM')
                        if os.path.exists(line[ptr + 2:ptr2]) is False:
                            # The name of directory can not have space!
                            os.mkdir(line[ptr + 2:ptr2])  # create the folder for each volume
                        os.chdir(line[ptr + 2:ptr2])  # go into that folder
                    else:  # always deal with exception
                        if os.path.exists(line[ptr + 2:-2]) is False:
                            # The name of directory can not have space!
                            os.mkdir(line[ptr + 2:-2])  # create the folder for each volume
                        os.chdir(line[ptr + 2:-2])  # go into that folder

                    mark = 3  # write saint= letter head file
                    # continue
                elif mark == 3 and line.find('|g') == -1:
                    fI = codecs.open('__LetterHeader.txt', 'a+', 'utf-8')
                    print(line)
                    fI.write(line)
                elif (mark == 3 or mark == 4) and line.find('|g') != -1:
                    if line.find('|g') != -1:  # find the individual song
                        # if(counter != 0): fmei.close()
                        line = line.replace(' ', '')
                        ptr2 = line.find('.')
                        mode = line[ptr2 + 1:ptr2 + 3]  # get the mode and tonal center
                        print(mode)
                        ptr = line.find('|g')
                        line = line.replace('?', '-')
                        line = line.replace('/', '-')
                        counter += 1  # num of songs
                        # print (counter)
                        signWriteToMei = False  # have not wrote to file
                        fsong = codecs.open(line[ptr + 1:-2] + '.txt', 'a+', 'utf-8')
                        endOfLyricsSign = False
                        endOfMelodySign = False  # Update the sign, since it is a new song!
                        # fmei=codecs.open(line[ptr+1:-2]+'.mei','a+','utf-8')
                        if counter != 1:  # change the title of the last song
                            # change_song_title(LastDir, FakeTitle, word, '.mei', ChangeDir)
                            change_song_title(LastDir, FakeTitle, word, '.txt', ChangeDir)
                            ChangeDir = False  # only deal with the last file in the last dir
                        FakeTitle = line[ptr + 1:-2]
                        # print (line)
                        print(line, file=fsong)
                        # print(line, file=log)
                        mark = 4  # write individual song
                        # continue
                elif (line.find('|.') == -1 and line.find('[File') == -1 and line.find('[file') == -1 and line.find(
                        '|g') == -1 and mark == 4):  # write lines into a txt file
                    # print (line)
                    signWriteToMei = True  # After writing this line, write to mei file
                    print(line, file=fsong)
                    if line[0:2] == '\ ' or line[2:4] == '\ ':  # this is melody with lyric line
                        print(line)
                    elif line[0:2] == '/ ' or line[2:4] == '/ ':  # lyric line
                        if line.find('pio festo') != -1:
                            print('continue')
                        if line[-4:-1] == '/()':  # this does not have exceptions so far
                            endOfLyricsSign = True  # It means the lyrics are complete
                        while line.find('/()') == -1 and endOfLyricsSign is False:  # nasty exceptions
                            newline = f1.readline()

                            print(newline, file=fsong)
                            line += newline
                        if line.find('luminI.1.1.1;') != -1:  # exception where his encoding is wrong
                            print("unsolved exception")
                        if line.find('/()') == -1 and endOfLyricsSign is True:  # Non-lyric line
                            print("ERROR!")
                        else:
                            for i in line:
                                if (i.isalpha() or i == ' ') is False:
                                    line = line.replace(i,
                                                        ' ')  # replace anything other than letter or space into a space
                                    # print(("lyric" + line))
                            line = line.replace('  ', ' ')  # multiple space is reduced to one
                            syllabifierNum = chunk_lyrics(line, word, syllable)
                line = f1.readline()
