 #-*- coding: utf-8 -*-
import os
import codecs
from cltk.stem.latin.syllabifier import Syllabifier
import sys
sys.path.append('/Users/yaolong/Documents/libmei/python/') #otherwise it can not be found!
import pymei

format=['txt']
counter=0
syllabus = [' ' for i in range (10000)]
word = [' ' for i in range (10000)]
numOfRealSyl = [0 for i in range(10000)]
numOfArtiSyl = [0 for i in range(10000)]
cwd = os.getcwd()
ChangeDir = False
syllabifier = Syllabifier()
log =open('SyllabifierLog.txt','w')
globalSign = False # for debug
endOfMelodySign = False
endOfLyricsSign = False # There will be exceptions where the line is not complete within a line
def change_song_title(lastdir, faketitle, word, type, changedir):
    '''
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
    '''

    for i in range(10000):
        if(word[i]==''):
            break
    length = i
    #print (length)
    LengthOfTitle = 5
    if(length<=LengthOfTitle):
        FinalLength = length
    else:
        FinalLength = LengthOfTitle
    for i in range(FinalLength): # assume that the title is no longer than 10 words
        if(word[i][-1].isupper()):
            break
    realtitle = ''
    for j in range(0,i+1):
        realtitle = realtitle + word[j]+'_'
    realtitle = realtitle.lower()
    if(changedir==True):
        if(os.path.isfile(os.path.join(lastdir, faketitle+type))):
            os.rename(os.path.join(lastdir, faketitle+type), os.path.join(lastdir, realtitle[1].upper()+realtitle[2:-1]+type))
    else:
        if(os.path.isfile(os.path.join(os.getcwd(), faketitle + type))):
            os.rename(os.path.join(os.getcwd(), faketitle + type), os.path.join(os.getcwd(), realtitle[1].upper() + realtitle[2:-1] + type)) # 0 is a space

def chunk_lyrics(lyrics, word, list):
    '''
    This function chunked the lyrics into syllables using a syllabifier from cltk toolkit
    :param lyrics: A string. The original lyrics line
    :param word: Array for strings. each stores a word forms the lyrics
    :param list: Array for strings, each stores a syllable
    :return:
    '''
    #lyrics = lyrics.lower()
    vowel = ['a','e','i','o','u']
    coounter = 0
    sign = 0
    numofSyllabus = 0
    numofWord = 0
    sumNumofSyl = 0
    begin = end = 0
    for i in range(1, len(lyrics)):
        if(lyrics[i] == ' '):
            if(begin!=end): #not the first space
                end = i - 1
                word[numofWord] = lyrics[begin:end+1]
                numofWord = numofWord + 1
                begin = i + 1
            else: begin = 1 # skip the first space
    for i in range(numofWord):
        #print (word[i])
        numofSyllabus = 0
        tmp = syllabifier.syllabify(word[i].lower())
        for element in tmp:
            list[sumNumofSyl] = element
            numofSyllabus = numofSyllabus + 1
            sumNumofSyl = sumNumofSyl + 1
        numOfArtiSyl[i] = numofSyllabus
    return sumNumofSyl

def print_measure(id, section):
    '''
    A function that creates measure element under <section> hierarchy.
    :param id: Integer, the id of the measure.
    :param section: The pymei object of <section>
    :return:
    '''
    measure = pymei.MeiElement('measure')
    staff = pymei.MeiElement('staff')
    layer = pymei.MeiElement('layer')
    section.addChild(measure)
    measure.addChild(staff)
    staff.addChild(layer)
    measure.addAttribute('n', '{}'.format(id))
    return layer

def add_note(pname, oct, layer):
    '''
    A function that creates notes element under <layer> hierarchy.
    :param pname: Char, pitch name
    :param oct: Int, octave of the note
    :param layer: The pymei object of <layer>, <note> is under it.
    :return:
    '''
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname','{}'.format(pname))
    note.addAttribute('oct', '{}'.format(oct))
    note.addAttribute('dur', '4')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    return note
def add_grace_note(pname, oct, layer):
    '''
    A function that creates grace notes element under <layer> hierarchy.
    :param pname: Char, pitch name
    :param oct: Int, octave of the note
    :param layer: The pymei object of <layer>
    :return:
        '''
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname','{}'.format(pname))
    note.addAttribute('oct', '{}'.format(oct))
    note.addAttribute('dur', '8')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    note.addAttribute('grace', 'acc')
    return note

def add_lyrics(note, syllable):
    '''
    A function that creates 'verse' and 'syl' hierarchy under 'note' and adds lyrics
    under <syl> hierarchy.
    :param note: The note object of pymei.
    :param syllable: The syllable to add to MEI file.
    :return:
    '''
    verse = pymei.MeiElement('verse')
    syl = pymei.MeiElement('syl')
    note.addChild(verse)
    verse.addAttribute('n','1')
    syl.setValue(syllable)
    verse.addChild(syl)

def add_lyrics2(note, syllable):
    '''
    Another function to add lyrics on note level, which does not work, though.
    '''
    note.addAttribute('syl','{}'.format(syllable))

def print_note(pitchid, octid, layer, ptr, status, syllabus, ptr2):
    '''
    Add notes to MEI stream
    :param pitchid: Char, pitch.
    :param octid: Int, octave.
    :param layer: A hirarchical layer before <note>.
    :param ptr: The id of note
    :param status: The status of the note: is it just note, or note attached with lyrics, or grace note.
    :param syllabus: The possible syllabus attached to the note
    :param ptr2: The id  of the syllabus
    :return:
    '''
    if(status[ptr]=='n'):
        if(len(status)-1>ptr):
            if(status[ptr+1]!='g'):
                add_note(pitchid[ptr], octid[ptr], layer)
    elif(status[ptr]=='g'): # grace note
        add_grace_note(pitchid[ptr-1], octid[ptr-1], layer)
    elif(status[ptr]=='l'): # syllabus
        if(len(status)-1>ptr):
            note = add_note(pitchid[ptr+1], octid[ptr+1], layer)
            add_lyrics(note, syllabus[ptr2])
        '''elif(status[ptr]=='s'):
             tmpPtr = ptr-1
             while(status[tmpPtr]=='n'):
                 tmpPtr = tmpPtr - 1
             tmpPtr = tmpPtr + 1
             noteNum = ptr - tmpPtr # get the number of notes in with a slur
             startSlur = measurePtr - noteNum
             endSlur = measurePtr
             newFid.write("< slur tstamp = \"%i\" tstamp2 = \"0m+%i\" curvedir = \"above\" / >\n"  % (measurePtr%4+1, noteNum))'''

'''def SearchMode(mode):
     if (mode == '1' or mode == '2'):
         return Dor
     elif (mode == '3' or mode == '4'):
         return Phr
     elif (mode == '5' or mode == '6'):
         return Lyd
     elif (mode == '7' or mode == '8'):
         return Mix'''
def num_to_pitch_class_with_oct(num, final, oct):
    '''
    Transform number into pitch-class, which is key-sensitive.
    :param num: Int, the number which the original encoding uses.
    :param final: The tonic center.
    :param oct: The octave array.
    :return: 
    '''
    Dict = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
     # mod = SearchMode(mode)
    for ptr in range(len(num)):
        for i in range(7):
            if (final == Dict[i]):
                 break
        if (num[ptr] == '>'):
            num = num[0:ptr] + '3' + num[ptr + 1:]
            oct[ptr] = oct[ptr] + 1
        elif (num[ptr] == '-'):
            num = num[0:ptr] + '6' + num[ptr + 1:]
            oct[ptr] = oct[ptr] - 1
        elif (num[ptr] == '0'):
            num = num[0:ptr] + '7' + num[ptr + 1:]

            oct[ptr] = oct[ptr] - 1
        elif (num[ptr] == '*'):
            num = num[0:ptr] + '5' + num[ptr + 1:]

            oct[ptr] = oct[ptr] - 1
        elif (num[ptr] == '%'):
            num = num[0:ptr] + '4' + num[ptr + 1:]
            oct[ptr] = oct[ptr] - 1
        elif (num[ptr] == '='):
            num = num[0:ptr] + num[ptr - 1] + num[ptr + 1:]
            oct[ptr] = oct[ptr - 1]
        if (num[ptr].isdigit()):# convert digit into pitch-class
            m = int(num[ptr]) # current digit
            ii = i
            for j in range(m - 1):
                i = i + 1
                ii = ii + 1
                if (ii >= 7):
                    oct[ptr] = oct[ptr] + 1
                    ii = ii % 7
                i = i % 7
            num = num[0:ptr] + Dict[i] + num[ptr + 1:]
    return (num, oct)

def melody_line_to_MEI_func(melody, input, syllabus):
    '''
    A conclusive function that uses several sub-functions to format MEI file.
    :param melody: The original melody line.
    :param input: Two chars that contain the modality and the tonic center.
    :param syllabus: The string array to store the syllables.
    :return: 
    '''
    doc = pymei.documentFromFile(cwd+'/Template.mei').getMeiDocument()
    ptr = 0
    mode = input[0]
    final = input[1]
    counterOfSyl= 0
    length = len(melody)
    PitchClass = [' ' for i in range (len(melody))]
    Oct = [4 for i in range (len(melody))]
    status = [' ' for i in range (len(melody))]  # 0 for grace note
    for i in range (length):
        if (melody[i] == ','):
            status[i] = 'g'
        elif(melody[i] == '.'):
            status[i] = 'l'
            counterOfSyl = counterOfSyl + 1
        elif(melody[i] == '\''):
            status[i] = 's' # ligature, represented by slur
        else:
            status[i] = 'n'
    (melody, Oct) = num_to_pitch_class_with_oct(melody, final, Oct)
    i = 0
    measurePtr = 0
    sections = doc.getElementsByName('section')
    section = sections[0] # fill in from here
    while(i<length):
        if(measurePtr%4==0 and measurePtr!=0):
            layer = print_measure(measurePtr/4+1, section)
        elif(measurePtr%4==0):
            layer = print_measure(measurePtr/4 + 1, section)
        print_note(melody, Oct, layer, i, status, syllabus, ptr)
        if(status[i]=='l'):
            i = i + 1
            ptr = ptr + 1
        if(i==length): # it is possible that the last one of status is l
            break
        if(status[i] == 'n' ):
            if(i<length-1):
                if (status[i+1] != 'g'):
                    measurePtr = measurePtr + 1
        i = i + 1
    pymei.documentToFile(doc, FakeTitle + '.mei')
    return (counterOfSyl, doc)

if __name__ == "__main__":
    for filex in os.listdir('.'):
        '''
        Main function, where the whole file hirarchy is built and the '.txt' and '.mei' files are
        generated.
        '''
        if os.path.isfile(filex) and (os.path.splitext(filex)[1][1:].lower() in format)== True:
            print (filex)
            mark=0 # not find a head yet
            f1=open(filex,'r', encoding='cp437') # the actual encoding is cp437, not iso8859!
            blank = f1.readline()
            while blank:
                blank = blank.replace('«', '<<')
                if((blank.find('[File')!=-1 or blank.find('[file')!=-1) and mark==0):
                    print (blank) #show all the volumes
                    blank = blank.replace(' ', '')  # The name of directory can not have space!
                    ptr=blank.find('CH-')
                    print(blank[ptr:ptr+4])
                    if(os.path.exists(blank[ptr:-2])==False):
                        if(blank.find('MDNM')!=-1): # MDNM is not wanted
                            ptr3 = blank.find('MDNM')
                            os.mkdir(blank[ptr:ptr3 - 2])# remove MDNM staff
                            os.chdir(blank[ptr:ptr3 - 2])
                        else:
                            os.mkdir(blank[ptr:-2])# create the folder for each volume
                            os.chdir(blank[ptr:-2])# go into that folder
                    mark=1 # write volumn file
                    #continue # read next line
                elif(blank.find('|.')==-1 and mark==1): # Not saint yet, it will be head instructions, save it into file
                    fI=codecs.open('instructions.txt','a+','utf-8')
                    fI.write(blank)
                elif(mark==1 and (blank.find('=')==-1 or blank.find('70=XCX')!=-1 or blank.find('8=0504')!=-1 or (blank.find('(')!=-1 and blank.find(')')!=-1) or blank.find('[Advent')!=-1) and blank.find('|.')!=-1): # find a saint, continue to create folder for that saint
                    #print (blank)
                    fI.close()
                    blank = blank.replace(' ', '_')  # The name of directory can not have space!
                    if(blank.find('X_') or blank.find('K_') !=-1):
                        if (blank.find('X_')!=-1): # try to find the name of the saint
                            ptr = blank.find('X_') + 2
                        elif(blank.find('K_')!=-1):# try to find the name of the saint
                            ptr = blank.find('K_') + 2
                        if(blank.find(')')!=-1):
                            ptr4 = blank.find(')') # only keep the saint's name
                            if (os.path.exists(blank[ptr:ptr4]) == False):  # create the folder of the saint s name
                                os.mkdir(blank[ptr:ptr4])
                            os.chdir(blank[ptr:ptr4])
                        else:
                            if (os.path.exists(blank[ptr:-1]) == False):#create the folder of the saint s name
                                os.mkdir(blank[ptr:-1])
                            os.chdir(blank[ptr:-1])
                        if (blank.find('|.') != -1):
                            ptr2 = blank.find('|.')
                            if(blank.find('_(')!=-1):
                                ptr3 = blank.find('_(')
                                if (os.path.exists(blank[ptr2 + 2:ptr3]) == False):  # ptr3 means only keep ANNA like file name
                                    os.mkdir(blank[ptr2 + 2:ptr3])  # then create the ID number of that saint
                                os.chdir(blank[ptr2 + 2:ptr3])
                            else:
                                if (os.path.exists(blank[ptr2 + 2:ptr - 2]) == False): # ptr3 means only keep ANNA like file name
                                    os.mkdir(blank[ptr2 + 2:ptr - 2])  # then create the ID number of that saint
                                os.chdir(blank[ptr2 + 2:ptr - 2])
                        else:  # always deal with exception
                            if (os.path.exists(blank[:ptr - 2]) == False):
                                os.mkdir(blank[:ptr - 2])  # then create the ID number of that saint
                            os.chdir(blank[:ptr - 2])
                    else: # if there is an exception, do as usual
                        ptr = blank.find('|.')
                        if (os.path.exists(blank[ptr + 2:-2]) == False):
                            os.mkdir(blank[ptr + 2:-2])
                        os.chdir(blank[ptr + 2:-2])
                        if (os.path.exists(blank[ptr + 2:-2]) == False):
                            os.mkdir(blank[ptr + 2:-2])
                        os.chdir(blank[ptr + 2:-2])
                    mark=2 # write saint file
                    #continue
                elif(mark==2 and blank.find('|.')==-1):
                    fI=codecs.open('instructions.txt','a+','utf-8')
                    #print (blank)
                    print(blank, file=fI)
                elif(mark==2 and blank.find('=')!=-1 and blank.find('|.')!=-1): #saint's name=letter
                    print (blank)
                    fI.close()
                    blank=blank.replace('"','-')
                    blank = blank.replace(' ', '')
                    blank = blank.replace('=L', '=Lauds')
                    blank = blank.replace('=M', '=Matins')
                    blank = blank.replace('=V', '=Vespers')
                    blank = blank.replace('=W', '=2nd_Vespers')
                    ptr=blank.find('|.')
                    if(blank.find('<<MDNM')!=-1):
                        ptr2 = blank.find('<<MDNM')
                        if (os.path.exists(blank[ptr + 2:ptr2]) == False):
                            # The name of directory can not have space!
                            os.mkdir(blank[ptr + 2:ptr2])  # create the folder for each volume
                        os.chdir(blank[ptr + 2:ptr2])  # go into that folder
                    else: #always deal with exception
                        if(os.path.exists(blank[ptr+2:-2])==False):
                          # The name of directory can not have space!
                            os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                        os.chdir(blank[ptr+2:-2])# go into that folder

                    mark=3 # write saint= letter head file
                    #continue
                elif(mark==3 and blank.find('|g')==-1):
                    fI=codecs.open('instructions.txt','a+','utf-8')
                    print (blank)
                    fI.write(blank)
                elif(mark==3 and blank.find('|g')!=-1):
                    if (blank.find('|g')!=-1): # find the individual song
                        #if(counter != 0): fmei.close()
                        blank = blank.replace(' ', '')
                        ptr2=blank.find('.')
                        mode=blank[ptr2+1:ptr2+3] # get the mode and tonal center
                        print (mode)
                        ptr=blank.find('|g')
                        blank=blank.replace('?','-')
                        counter = counter + 1 # num of songs
                        #print (counter)
                        signWriteToMei = False # have not wrote to file
                        fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                        endOfLyricsSign = False
                        endOfMelodySign = False # Update the sign, since it is a new song!
                        #fmei=codecs.open(blank[ptr+1:-2]+'.mei','a+','utf-8')
                        if (counter != 1):  # change the title of the last song
                            change_song_title(LastDir,FakeTitle, word, '.mei', ChangeDir)
                            change_song_title(LastDir,FakeTitle, word, '.txt', ChangeDir)
                            ChangeDir = False # only deal with the last file in the last dir
                        FakeTitle = blank[ptr + 1:-2]
                        #print (blank)
                        print(blank, file=fsong)
                        print(blank, file=log)
                        mark=4 # write individual song
                        #continue
                elif(blank.find('|.')==-1 and blank.find('[File')==-1 and blank.find('[file')==-1 and blank.find('|g')==-1 and mark==4): #write lines into a txt file
                    #print (blank)
                    signWriteToMei = True #After writing this line, write to mei file
                    print(blank, file=fsong)
                    if (blank[0:2]=='\ ' or blank[2:4]=='\ '):  # this is melody with lyric line
                        #print(blank)

                        if(blank[-4:-1]=='\()'): # This ensures that the melody line is finished
                            endOfMelodySign = True
                        if(globalSign==True):

                            while(blank.find('\()')==-1 and endOfMelodySign==False): # nasty exceptions
                                newblank = f1.readline()


                                print(newblank, file=fsong)
                                blank = blank + newblank # read new line and append to the original until the end
                            if(blank.find('\()')==-1 and endOfMelodySign==True): #exceptions!
                                print("error") # There are occasions where there is more than one
                                               # melody lines,
                                if(blank.find('\(ve)')!=-1): # deal with exceptions case by case
                                    blank = f1.readline() # discard this line, since it is not a melody line
                                    continue
                                if (blank.find('(v in Sarum) ??') != -1):
                                    blank = f1.readline()  # discard this line, since it is not a melody line
                                    continue
                                if (blank.find('et.21,=0') != -1):
                                    blank = f1.readline()  # discard this line, since it is not a melody line
                                    continue
                        blank = blank.replace('\\', '')
                        blank = blank.replace('#', '')
                        blank = blank.replace('(', '')
                        blank = blank.replace(')', '')
                        blank = blank.replace('<', '') # there might be < in the text, really need a complete examination!!!
                        blank = blank.replace('\r', '')
                        blank = blank.replace('\n', '')
                        blank = blank.replace('?', '')
                        blank = blank.replace('+', '')
                        blank = blank.replace('v', '')
                        blank = blank.replace(';', '')
                        blank = blank.replace('$', '')
                        blank = blank.replace('^', '')
                        blank = blank.replace('!', '')
                        blank = blank.replace('  ', ' ')
                        # count the syllables for each word
                        numOfDot = 0
                        numofWord = 0
                        for i in range(1, len(blank)):
                            if (blank[i] == '.'):
                                numOfDot = numOfDot + 1
                            elif (blank[i] == ' '):  # last word ends, new word begins
                                numOfRealSyl[numofWord] = numOfDot
                                numofWord = numofWord + 1
                                numOfDot = 0
                                # end
                        for i in range(len(blank)):
                            if(blank[i].isalpha()):
                                blank = blank.replace(blank[i],' ')
                        blank = blank.replace(' ', '')
                        #print(('melody'+blank))
                        (realSyllableNum, doc) = melody_line_to_MEI_func(blank, mode, syllabus)#blank2 = blank.replace('.', '')  # melody with syllabus sign
                        if (realSyllableNum != syllabifierNum):
                            print("Total num of syllables from Andrew     : ", realSyllableNum, file=log)
                            print("Total num of syllables from Syllabifier: ", syllabifierNum, file=log)
                            for i in range(numofWord):
                                syllabifier.syllabify(word[i])
                                if(numOfRealSyl[i]!=numOfArtiSyl[i]):#only output different ones
                                    print(word[i], file=log)
                                    print(numOfRealSyl[i], file=log)
                                    print(numOfArtiSyl[i], "results of Syllabifier:", syllabifier.syllabify(word[i]), file=log)
                            #str = input("What do you think about it?")
                            #print(str)
                        #blank = blank.replace(',', '')
                    elif(blank[0:2]=='/ ' or blank[2:4]=='/ '): # lyric line
                        if(blank.find('pio festo')!=-1):
                            print ('continue')
                        if(blank[-4:-1]=='/()'): # this does not have exceptions so far
                            endOfLyricsSign = True # It means the lyrics are complete
                        while (blank.find('/()')==-1 and endOfLyricsSign==False):  # nasty exceptions
                            newblank = f1.readline()

                            print(newblank, file=fsong)
                            blank = blank + newblank
                        if (blank.find('luminI.1.1.1;') != -1): # exception where his encoding is wrong
                            print("unsolved exception")
                        if(blank.find('/()')==-1 and endOfLyricsSign==True): # Non-lyric line
                            print ("ERROR!")
                        else:
                             for i in range(len(blank)):
                                if((blank[i].isalpha() or blank[i] == ' ')==False):
                                    blank = blank.replace(blank[i],' ') # replace anything other than letter or space into a space
                        #print(("lyric" + blank))
                             blank = blank.replace('  ', ' ') # multiple space is reduced to one
                             syllabifierNum = chunk_lyrics(blank, word, syllabus)
                elif(mark==4):
                        if(blank.find('[File')!=-1 or blank.find('[file')!=-1):
                             # find a volume
                            #print (blank) #show all the volumes
                            blank = blank.replace(' ', '')
                            ptr=blank.find('CH-')
                            print(blank[ptr:ptr + 4])
                            if (blank[ptr:ptr + 4] == 'CH-C'):
                                print("alert")
                                globalSign = True
                                #tmp = input("What do you think about it")
                            LastDir = os.getcwd()
                            ChangeDir = True
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                            os.chdir(os.pardir)
                            if (os.path.exists(blank[ptr:-2]) == False):
                                 if (blank.find('MDNM') != -1):  # MDNM is not wanted
                                     ptr3 = blank.find('MDNM')
                                     os.mkdir(blank[ptr:ptr3 - 2])
                                     os.chdir(blank[ptr:ptr3 - 2])
                                 else:
                                    os.mkdir(blank[ptr:-2])  # create the folder for each volume
                                    os.chdir(blank[ptr:-2])# go into that folder
                            mark=1
                            #continue # read next line
                        elif((blank.find('=')==-1 or blank.find('70=XCX')!=-1 or blank.find('8=0504')!=-1 or (blank.find('(')!=-1 and blank.find(')')!=-1) or blank.find('[Advent')!=-1) and blank.find('|.')!=-1): # Not saint yet, it will be head instructions, save it into file
                            #print (blank)
                            blank = blank.replace(' ', '_')
                            blank = blank.replace('\t', '-')
                            blank = blank.replace('"', '-')
                            if (blank.find('X_') or blank.find('K_') != -1):
                                LastDir = os.getcwd()
                                ChangeDir = True
                                os.chdir(os.pardir)
                                os.chdir(os.pardir)
                                os.chdir(os.pardir)
                                if (blank.find('X_') != -1):  # try to find the name of the saint
                                    ptr = blank.find('X_') + 2
                                elif (blank.find('K_') != -1):  # try to find the name of the saint
                                    ptr = blank.find('K_') + 2
                                if (blank.find(')') != -1):
                                    ptr4 = blank.find(')')  # only keep the saint's name
                                    if (os.path.exists(blank[ptr:ptr4]) == False):  # create the folder of the saint s name
                                        os.mkdir(blank[ptr:ptr4])
                                    os.chdir(blank[ptr:ptr4])
                                else:
                                    if (os.path.exists(blank[ptr:-1]) == False):  # create the folder of the saint s name
                                        os.mkdir(blank[ptr:-1])
                                    os.chdir(blank[ptr:-1])
                                if (blank.find('|.') != -1):
                                    ptr2 = blank.find('|.')
                                    if (blank.find('_(') != -1):
                                        ptr3 = blank.find('_(')
                                        if (os.path.exists(
                                                blank[ptr2 + 2:ptr3]) == False):  # ptr3 means only keep ANNA like file name
                                            os.mkdir(blank[ptr2 + 2:ptr3])  # then create the ID number of that saint
                                        os.chdir(blank[ptr2 + 2:ptr3])
                                    else:
                                        if (os.path.exists(blank[
                                                           ptr2 + 2:ptr - 2]) == False):  # ptr3 means only keep ANNA like file name
                                            os.mkdir(blank[ptr2 + 2:ptr - 2])  # then create the ID number of that saint
                                        os.chdir(blank[ptr2 + 2:ptr - 2])
                                else:  # always deal with exception
                                    if (os.path.exists(blank[:ptr - 2]) == False):
                                        os.mkdir(blank[:ptr - 2])  # then create the ID number of that saint
                                    os.chdir(blank[:ptr - 2])
                            else:  # if there is an exception, do as usual
                                ptr = blank.find('|.')
                                LastDir = os.getcwd()
                                ChangeDir = True
                                os.chdir(os.pardir)
                                os.chdir(os.pardir)
                                os.chdir(os.pardir)
                                if (os.path.exists(blank[ptr + 2:-2]) == False):
                                    os.mkdir(blank[ptr + 2:-2])
                                os.chdir(blank[ptr + 2:-2])
                            mark=2 # write saint file
                            #continue
                        elif(blank.find('|.')!=-1 and blank.find('=')!=-1): #saint's name=letter
                            #print (blank)
                            print(blank, file=log)
                            blank = blank.replace(' ', '')
                            ptr=blank.find('|.')
                            blank=blank.replace('?','-')
                            blank=blank.replace('/','-')
                            blank=blank.replace('"','-')
                            blank = blank.replace('=L', '=Lauds')
                            blank = blank.replace('=M', '=Matins')
                            blank = blank.replace('=V', '=Vespers')
                            blank = blank.replace('=W', '=2nd_Vespers')
                            LastDir = os.getcwd()
                            ChangeDir = True
                            os.chdir(os.pardir)
                            if (blank.find('<<MDNM') != -1):
                                ptr2 = blank.find('<<MDNM')
                                if (os.path.exists(blank[ptr + 2:ptr2]) == False):
                                    # The name of directory can not have space!
                                    os.mkdir(blank[ptr + 2:ptr2])  # create the folder for each volume
                                os.chdir(blank[ptr + 2:ptr2])  # go into that folder
                            else:  # always deal with exception
                                if (os.path.exists(blank[ptr + 2:-2]) == False):
                                    # The name of directory can not have space!
                                    os.mkdir(blank[ptr + 2:-2])  # create the folder for each volume
                                os.chdir(blank[ptr + 2:-2])  # go into that folder
                            mark=3 # write saint= letter head file
                            #continue
                            #print type(blank)
                            #print unicode(blank)
                            #os.mkdir(blank)'''
                        elif(blank.find('|g')!=-1):
                            #if (counter != 0): fmei.close()
                            blank = blank.replace(' ', '')
                            ptr2 = blank.find('.')
                            mode = blank[ptr2 + 1:ptr2 + 3]  # get the mode and tonal center
                            print(mode)
                            ptr=blank.find('|g')
                            blank=blank.replace('?','-')
                            blank=blank.replace('/','-')
                            counter = counter + 1 # num of songs
                            #print (counter)
                            print (blank[ptr+1:-2])
                            print(blank[ptr+1:-2], file=log)

                            signWriteToMei = False # have not wrote to file
                            fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                            endOfLyricsSign = False
                            endOfMelodySign = False  # Update the sign, since it is a new song!
                            #fmei = codecs.open(blank[ptr + 1:-2] + '.mei', 'a+', 'utf-8')
                            if (counter != 1):  # change the title of the last song
                                change_song_title(LastDir, FakeTitle, word, '.mei', ChangeDir)
                                change_song_title(LastDir, FakeTitle, word, '.txt', ChangeDir)
                                ChangeDir = False # only change the last file of the last dir
                            FakeTitle = blank[ptr+1:-2]
                            #print (blank)
                            print(blank, file=fsong)
                            mark=4 # write individual song
                            #continue
                blank = f1.readline()