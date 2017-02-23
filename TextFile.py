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
            if not ASCII.isalpha():
                line = line.replace(ASCII, '')
    return line
def change_song_title(faketitle, word, type, counter):
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
    if os.path.isfile(os.path.join(os.getcwd(), faketitle + type)):
        if os.path.isfile(os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type)) == False: # if the read title does not exist
            #print(os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type))
            os.rename(os.path.join(os.getcwd(), faketitle + type),
        os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + type))  # 0 is a space
        else:
            os.rename(os.path.join(os.getcwd(), faketitle + type),
                      os.path.join(os.getcwd(), realtitle[0].upper() + realtitle[1:-1] + '_' + str(counter) + type))  # 0 is a space, if the
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

if __name__ == "__main__":
    format = ['txt']
    counter = 0
    numOfSameFileName = 0
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
            os.mkdir('AllTextFiles')
            os.chdir('AllTextFiles')
            while line:
                line = line.replace('«', '<<')
                if line.find('|g') != -1 and line.find('=') != -1 and line.find('.') != -1:# find the individual song
                        # if(counter != 0): fmei.close()
                        line = line.replace(' ', '')
                        ptr2 = line.find('.')
                        mode = line[ptr2 + 1:ptr2 + 3]  # get the mode and tonal center
                        #print(mode)
                        ptr = line.find('|g')
                        line = line.replace('?', '-')
                        line = line.replace('/', '-')
                        counter += 1  # num of songs
                        # print (counter)
                        signWriteToMei = False  # have not wrote to file
                        tmpTitle = line[ptr + 1:-2]
                        if tmpTitle.find('(') != -1: # exception: the title can append a very long message within ()
                            ptr3 = tmpTitle.find('(')
                            tmpTitle = tmpTitle[0:ptr3] + tmpTitle[-2:-1]
                            # trick, since if the information within () is cut off, some file name will be the same,
                            # and it will cause prob
                        print(tmpTitle)
                        fsong = codecs.open(tmpTitle + '.txt', 'a+', 'utf-8')
                        if counter != 1:
                            numOfSameFileName = change_song_title(FakeTitle, word, '.txt', numOfSameFileName) # change the name of the last file!
                        FakeTitle = tmpTitle
                        endOfLyricsSign = False
                        endOfMelodySign = False  # Update the sign, since it is a new song!
                        # fmei=codecs.open(line[ptr+1:-2]+'.mei','a+','utf-8')
                        if counter != 1:  # change the title of the last song
                            # change_song_title(LastDir, FakeTitle, word, '.mei', ChangeDir)
                            #change_song_title(LastDir, FakeTitle, word, '.txt', ChangeDir)
                            ChangeDir = False  # only deal with the last file in the last dir

                        # print (line)
                        print(line, file=fsong, end='')
                        # print(line, file=log)
                        mark = 1  # write individual song
                        # continue
                elif (line.find('|.') == -1 and line.find('[File') == -1 and line.find('[file') == -1 and line.find(
                        '|g') == -1 and mark == 1):  # write lines into a txt file
                    # print (line)
                    signWriteToMei = True  # After writing this line, write to mei file
                    print(line, file=fsong, end='')
                    #if line[0:2] == '\ ' or line[2:4] == '\ ':  # this is melody with lyric line
                        #print(line)
                    if line[0:2] == '/ ' or line[2:4] == '/ ':  # lyric line
                        pointer = line.find('/ ') # for exception: some lines begins with space than '/ '
                        syllabifierNum = chunk_lyrics(line[pointer:], word, syllable)

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
                else:
                    mark = 0
                line = f1.readline()
