# -*- coding: utf-8 -*-
__author__ = "Yaolong Ju (yaolong.ju@mail.mcgill.ca)"
__date__ = "2017"
import os
import codecs
from cltk.stem.latin.syllabifier import Syllabifier

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
def change_song_title(lastdir, faketitle, word, type, changedir, counter, flag):
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

    return counter
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
    Generate the hierarchical folders
    :param line: The current line which contained the desired name of the folder
    :param ptr1: The pointer which points the beginning of the file name
    :param ptr2: The pointer which points the end of the file name
    :return:
    """
    folder_name = line[ptr1:ptr2]
    folder_name = regulate_name('_.=()-', folder_name) # Make sure that the file name is compatible with Windows
    if os.path.exists(folder_name) is False:
        # The name of directory can not have space!
        os.mkdir(folder_name)  # create the folder for each volume
    os.chdir(folder_name)  # go into that folder

def parse(filex, flag1, flag2, flag3):
    """
    The function that parses the original file with Hughes' encodings.
    :param filex: The file pointer that points to the original file
    :param flag1: Whether to generate the file structure
    :param flag2: Whether to generate the text file
    :param flag3: Whether to generate the MEI file
    :return:
    """
    counter = 0
    numOfSameFileName = 0
    syllable = [' ' for i in range(10000)]
    word = [' ' for i in range(10000)]
    numOfRealSyl = [0 for i in range(10000)]
    melodyLine = ['%', '*', '-', '>', '.', '\'', '=', ',',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']  # char we need from melody line
    cwd = os.getcwd()

    ChangeDir = False

    # log = open('SyllabifierLog.txt', 'w')
    # globalSign = False  # for debug
    endOfMelodySign = False
    endOfLyricsSign = False  # There will be exceptions where the line is not complete within a line
    print(filex)
    mark = 0  # not find a head yet
    f1 = open(filex, 'r', encoding='cp437')  # the actual encoding is cp437, not iso8859!
    line = f1.readline()
    if (flag1 == 0):
        if os.path.exists("AllTextFiles") is False:
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
                        generate_file_structure(line, ptr, ptr4)
                else:
                    if (flag1 == 1):
                        generate_file_structure(line, ptr, -1)
                if line.find('|.') != -1:
                    ptr2 = line.find('|.')
                    if line.find('_(') != -1:
                        ptr3 = line.find('_(')
                        if (flag1 == 1):
                            generate_file_structure(line, ptr2 + 2, ptr3)
                    else:
                        if (flag1 == 1):
                            generate_file_structure(line, ptr2 + 2, ptr - 2)
                else:  # always deal with exception
                    if (flag1 == 1):
                        generate_file_structure(line, 0, ptr - 2)
            else:  # if there is an exception, do as usual
                ptr = line.find('|.')
                if (mark == 4):
                    LastDir = os.getcwd()
                    ChangeDir = True
                    if (flag1 == 1):
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        generate_file_structure(line, ptr + 2, -2)
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
            ptr = line.find('|.')
            if (mark == 4):
                LastDir = os.getcwd()
                ChangeDir = True
                if (flag1 == 1):
                    os.chdir(os.pardir)
            if line.find('<<MDNM') != -1:
                ptr2 = line.find('<<MDNM')
                if (flag1 == 1):
                    generate_file_structure(line, ptr + 2, ptr2)
            else:  # always deal with exception
                if (flag1 == 1):
                    generate_file_structure(line, ptr + 2, -2)

            mark = 3  # write saint= letter head file
            # continue
        elif mark == 3 and line.find('|g') == -1:
            if flag1 == 1 and flag2 == 1:
                fI = codecs.open('__LetterHeader.txt', 'a+', 'utf-8')
                print(line)
                fI.write(line)
        elif (mark == 3 or mark == 4) and line.find('|g') != -1 and line.find('=') != -1 and line.find('.') != -1:
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
                print (counter)
                signWriteToMei = False  # have not wrote to file
                tmpTitle = line[ptr + 1:-2]
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
                        numOfSameFileName = change_song_title(LastDir, FakeTitle, word, '.txt', ChangeDir,
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
            signWriteToMei = True  # After writing this line, write to mei file
            if(flag2 == 1):
                print(line, file=fsong, end='')
            if line[0:2] == '\ ' or line[2:4] == '\ ':  # this is melody with lyric line
                print(line)
            elif line[0:2] == '/ ' or line[2:4] == '/ ':  # lyric line
                pointer = line.find('/ ')  # for exception: some lines begins with space than '/ '
                syllabifierNum = chunk_lyrics(line[pointer:], word, syllable)
                if line.find('pio festo') != -1:
                    print('continue')
                if line[-4:-1] == '/()':  # this does not have exceptions so far
                    endOfLyricsSign = True  # It means the lyrics are complete
                while line.find('/()') == -1 and endOfLyricsSign is False:  # nasty exceptions
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
                        if (i.isalpha() or i == ' ') is False:
                            line = line.replace(i,
                                                ' ')  # replace anything other than letter or space into a space
                            # print(("lyric" + line))
                    line = line.replace('  ', ' ')  # multiple space is reduced to one
        line = f1.readline()

if __name__ == "__main__":
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
            #flag1 = int(input("Generate file structure?"))
            #flag2 = int(input("Generate text files?"))
            #flag3 = int(input("Generate MEI structure?"))
            flag1 = 0
            flag2 = 1
            flag3 = 0
            parse(filex, flag1, flag2, flag3)