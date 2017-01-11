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

def ChangeSongTitle(lastdir, faketitle, word, type, changedir):
    for i in range(10000):
        if(word[i]==''):
            break
    length = i
    print (length)
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
        if(os.path.isfile(lastdir+'/'+faketitle+type)):
            os.rename(lastdir+'/'+faketitle+type,lastdir+'/'+realtitle[1].upper()+realtitle[2:-1]+type)
    else:
        if(os.path.isfile(os.getcwd() + '/' + faketitle + type)):
            os.rename(os.getcwd() + '/' + faketitle + type, os.getcwd() + '/' +realtitle[1].upper() + realtitle[2:-1] + type) # 0 is a space


def ChunkLyrics(lyrics, word, list):
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
                #word[numofWord] = word[numofWord].lower() # lower the case so that cltk syl can work!
                numofWord = numofWord + 1
                begin = i + 1
            else: begin = 1 # skip the first space

    for i in range(numofWord):
        #print (word[i])
        numofSyllabus = 0
        tmp = syllabifier.syllabify(word[i].lower())
        #print (syllabifier.syllabify(word[i]))
        for element in tmp:
            list[sumNumofSyl] = element
            numofSyllabus = numofSyllabus + 1
            sumNumofSyl = sumNumofSyl + 1
        numOfArtiSyl[i] = numofSyllabus
    return sumNumofSyl







def WriteToFile(originalFname, newFid):
     originalFid = open(originalFname, 'r')

     for line in originalFid.readlines():
         # print line
         newFid.write(line + '\n')
     originalFid.close()


def PrintMeasure(id, doc, section):
     # print ("<measure n=\"%i\" >" %id)
     # print ("<staff>\n")
     # print ("<layer>\n")
     measure = pymei.MeiElement('measure')
     staff = pymei.MeiElement('staff')
     layer = pymei.MeiElement('layer')
     section.addChild(measure)
     measure.addChild(staff)
     staff.addChild(layer)
     measure.addAttribute('n', '%i' % id)
     #newFid.write("\n <measure n=\"%i\" >\n" % id)
     #newFid.write("<staff>\n")
     #newFid.write("<layer>\n")
     return layer
def AddNote(pname, oct, layer):
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname','%c' %pname)
    note.addAttribute('oct', '%i' %oct)
    note.addAttribute('dur', '4')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    return note
def AddGraceNote(pname, oct, layer):
    note = pymei.MeiElement('note')
    layer.addChild(note)
    note.addAttribute('pname','%c' %pname)
    note.addAttribute('oct', '%i' %oct)
    note.addAttribute('dur', '8')
    note.addAttribute('stem.dir', 'up')
    note.addAttribute('stem.len', '0')
    note.addAttribute('grace', 'acc')
    return note
def AddLyrics(note, syllable):
    verse = pymei.MeiElement('verse')
    syl = pymei.MeiElement('syl')
    note.addChild(verse)

    verse.addAttribute('n','1')
    syl.tail='%s' % syllable
    verse.addChild(syl)

def AddLyrics2(note, syllable):
    note.addAttribute('syl','%s' % syllable)



def PrintNote(pitchid, octid, doc, layer, ptr, status, syllabus, ptr2, measurePtr):
     # print ("<note pname=\"%s\" oct=\"%i\" dur=\"4\" stem.dir=\"up\"> </note>" % (pitchid,octid))


         if(status[ptr]=='n'):
             if(len(status)-1>ptr):
                 #print (len(status))
                 #print(ptr)
                 if(status[ptr+1]!='g'):
                     AddNote(pitchid[ptr], octid[ptr], layer)
                    #newFid.write("<note pname=\"%s\" oct=\"%i\" dur=\"4\" stem.dir=\"up\" stem.len=\"0\"> </note>\n" % (pitchid[ptr], octid[ptr]))
         elif(status[ptr]=='g'): # grace note
            #newFid.write("<note pname=\"%s\" grace=\"acc\" oct=\"%i\" dur=\"8\" stem.dir=\"up\" stem.len=\"0\"> </note>\n" % (pitchid[ptr-1], octid[ptr-1]))
            AddGraceNote(pitchid[ptr-1], octid[ptr-1], layer)
         elif(status[ptr]=='l'): # syllabus
             if(len(status)-1>ptr):
                #newFid.write("<note pname=\"%s\" oct=\"%i\" dur=\"4\" stem.dir=\"up\" stem.len=\"0\">\n " % (pitchid[ptr+1], octid[ptr+1]))
                note = AddNote(pitchid[ptr+1], octid[ptr+1], layer)
                AddLyrics2(note, syllabus[ptr2])
                #newFid.write("<verse n=\"1\">\n")
                #newFid.write("<syl>%s</syl>\n" % syllabus[ptr2])
                #newFid.write("</verse>\n")
                #newFid.write("</note>\n")

         '''elif(status[ptr]=='s'):
             tmpPtr = ptr-1
             while(status[tmpPtr]=='n'):
                 tmpPtr = tmpPtr - 1
             tmpPtr = tmpPtr + 1
             noteNum = ptr - tmpPtr # get the number of notes in with a slur
             startSlur = measurePtr - noteNum
             endSlur = measurePtr

             newFid.write("< slur tstamp = \"%i\" tstamp2 = \"0m+%i\" curvedir = \"above\" / >\n"  % (measurePtr%4+1, noteNum))'''


         #return (ptr, ptr2)

'''def SearchMode(mode):
     if (mode == '1' or mode == '2'):
         return Dor
     elif (mode == '3' or mode == '4'):
         return Phr
     elif (mode == '5' or mode == '6'):
         return Lyd
     elif (mode == '7' or mode == '8'):
         return Mix'''


def NumToPitchClassWithOct(num, mode, final, oct):
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
             # debug
             # elif (num[ptr] == ','):
             # status[ptr - 1] = 'g'  # the last note is grace note
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
def MelodyLineToMEIFunc(melody, input, syllabus):
    doc = pymei.documentFromFile(cwd+'/Template.mei').getMeiDocument()
    ptr = 0
    mode = input[0]
    final = input[1]

    counterOfSyl= 0
    length = len(melody)
    PitchClass = [' ' for i in range (len(melody))]
    Oct = [4 for i in range (len(melody))]

    status = [' ' for i in range (len(melody))]  # 0 for grace note
    #WriteToFile(cwd+r'/TemplateHeadMeterless.txt',newFid)


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

    #melody = melody.replace(".", '')
    #melody = melody.replace(",", '')
    (melody, Oct) = NumToPitchClassWithOct(melody, mode, final, Oct)
    i = 0
    measurePtr = 0

    sections = doc.getElementsByName('section')
    section = sections[0] # fill in from here
    while(i<length):

        if(measurePtr%4==0 and measurePtr!=0):# wrong, bug
            #print ("</measure>")
            #newFid.write("</layer>\n")
            #newFid.write("</staff>\n")
            #newFid.write("</measure>\n")


            #PrintMeasure(measurePtr/4+1, newFid)
            layer = PrintMeasure(measurePtr/4+1, doc, section)
        elif(measurePtr%4==0):
            layer = PrintMeasure(measurePtr/4 + 1, doc, section)
        #print melody[i]
        #print NumToPitchClassWithOct(melody[i], mode, final, oct)

        PrintNote(melody, Oct, doc, layer, i, status, syllabus, ptr, measurePtr)
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

    #print "</measure>"
    #newFid.write("</layer>\n")
    #newFid.write("</staff>\n")
    #newFid.write("</measure>\n")


    #WriteToFile(cwd+r'/TemplateBottom.txt',newFid)
    pymei.documentToFile(doc, FakeTitle + '.mei')
    return (counterOfSyl, doc)
    #print PitchClass
    #print Oct
    #measure = length/4+1
    #print measure
    #os.system("pause")













for filex in os.listdir('.'):
    if os.path.isfile(filex) and (os.path.splitext(filex)[1][1:].lower() in format)== True:
        print (filex)
        mark=0 # not find a head yet
        f1=open(filex,'r', encoding='cp437') # the actual encoding is cp437, not iso8859!
        for blank in f1.readlines():
            #print (type(blank))
            #blank = bytes(blank, 'utf-8')
            #print (blank)
            blank = blank.replace('«', '<<')
           # blank = blank.decode("iso8859")
            if((blank.find('[File')!=-1 or blank.find('[file')!=-1) and mark==0):

                #print (blank) #show all the volumes
                blank = blank.replace(' ', '')  # The name of directory can not have space!
                ptr=blank.find('CH-')
                #blankT=blank.decode("ascii").encode("utf-8")

                #print chardet.detect(blank)
                if(os.path.exists(blank[ptr:-2])==False):
                    if(blank.find('MDNM')!=-1): # MDNM is not wanted
                        ptr3 = blank.find('MDNM')
                        os.mkdir(blank[ptr:ptr3 - 2])# remove MDNM staff
                        os.chdir(blank[ptr:ptr3 - 2])
                    else:
                        os.mkdir(blank[ptr:-2])# create the folder for each volume
                        os.chdir(blank[ptr:-2])# go into that folder
                mark=1 # write volumn file
                continue # read next line
            elif(blank.find('|.')==-1 and mark==1): # Not saint yet, it will be head instructions, save it into file

                fI=codecs.open('instructions.txt','a+','utf-8')


                #print (blank)

                fI.write(blank)

            elif(mark==1 and (blank.find('=')==-1 or blank.find('70=XCX')!=-1 or blank.find('8=0504')!=-1 or (blank.find('(')!=-1 and blank.find(')')!=-1) or blank.find('[Advent')!=-1) and blank.find('|.')!=-1): # find a saint, continue to create folder for that saint
                #print (blank)
                fI.close()
                blank = blank.replace(' ', '_')  # The name of directory can not have space!
                '''ptr=blank.find('|.')
                if(os.path.exists(blank[ptr+2:-2])==False):

                    os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                os.chdir(blank[ptr+2:-2])# go into that folder'''

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
                continue
            elif(mark==2 and blank.find('|.')==-1):

                fI=codecs.open('instructions.txt','a+','utf-8')

                #print (blank)
                print(blank, file=fI)
            elif(mark==2 and blank.find('=')!=-1 and blank.find('|.')!=-1): #saint's name=letter
                #print (blank)
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
                continue
            elif(mark==3 and blank.find('|g')==-1):
                fI=codecs.open('instructions.txt','a+','utf-8')


                #print (blank)

                fI.write(blank)
            elif(mark==3 and blank.find('|g')!=-1):
                if (blank.find('|g')!=-1): # find the individual song
                    #if(counter != 0): fmei.close()
                    blank = blank.replace(' ', '')
                    ptr2=blank.find('.')
                    mode=blank[ptr2+1:ptr2+3]
                    ptr=blank.find('|g')
                    blank=blank.replace('?','-')
                    counter = counter + 1 # num of songs
                    #print (counter)
                    signWriteToMei = False # have not wrote to file
                    fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                    #fmei=codecs.open(blank[ptr+1:-2]+'.mei','a+','utf-8')
                    if (counter != 1):  # change the title of the last song

                        ChangeSongTitle(LastDir,FakeTitle, word, '.mei', ChangeDir)
                        ChangeSongTitle(LastDir,FakeTitle, word, '.txt', ChangeDir)
                        ChangeDir = False # only deal with the last file in the last dir
                    FakeTitle = blank[ptr + 1:-2]
                    print (blank)
                    print(blank, file=fsong)
                    print(blank, file=log)


                    mark=4 # write individual song
                    continue
            elif(blank.find('|.')==-1 and blank.find('[File')==-1 and blank.find('[file')==-1 and blank.find('|g')==-1 and mark==4): #write lines into a txt file
                #print (blank)
                signWriteToMei = True #After writing this line, write to mei file
                print(blank, file=fsong)
                if (blank[0:2] == '\ '):  # this is melody with lyric line
                    #print(blank)


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

                    (realSyllableNum, doc) = MelodyLineToMEIFunc(blank, mode, syllabus)#blank2 = blank.replace('.', '')  # melody with syllabus sign
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
                elif(blank[0:2]=='/ '): # lyric line
                    for i in range(len(blank)):
                         if((blank[i].isalpha() or blank[i] == ' ')==False):
                             blank = blank.replace(blank[i],' ')
                    #print(("lyric" + blank))
                    syllabifierNum = ChunkLyrics(blank, word, syllabus)

                '''else:# other lines
                    if(signWriteToMei==True):
                        pymei.documentToFile(doc,FakeTitle+'.mei') #write to file once
                        signWriteToMei = False''' # already write to file






            elif(mark==4):

                    if(blank.find('[File')!=-1 or blank.find('[file')!=-1):
                         # find a volume
                        #print (blank) #show all the volumes
                        blank = blank.replace(' ', '')
                        ptr=blank.find('CH-')
                        #blankT=blank.decode("ascii").encode("utf-8")

                        #print chardet.detect(blank)
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
                        continue # read next line
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
                        #ptr=blank.find('|.')
                        #os.chdir(os.pardir)
                        #os.chdir(os.pardir)


                        #if(os.path.exists(blank[ptr+2:-2])==False):
                              # The name of directory can not have space!
                            #os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                        #os.chdir(blank[ptr+2:-2])# go into that folder
                        mark=2 # write saint file
                        continue


                    elif(blank.find('|.')!=-1 and blank.find('=')!=-1): #saint's name=letter
                        print (blank)
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
                        continue
                        #print type(blank)
                        #print unicode(blank)
                        #os.mkdir(blank)'''
                    elif(blank.find('|g')!=-1):
                        #if (counter != 0): fmei.close()
                        blank = blank.replace(' ', '')
                        ptr=blank.find('|g')
                        blank=blank.replace('?','-')
                        blank=blank.replace('/','-')
                        counter = counter + 1 # num of songs
                        #print (counter)
                        print (blank[ptr+1:-2])
                        print(blank[ptr+1:-2], file=log)
                        signWriteToMei = False # have not wrote to file
                        fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                        #fmei = codecs.open(blank[ptr + 1:-2] + '.mei', 'a+', 'utf-8')
                        if (counter != 1):  # change the title of the last song
                            ChangeSongTitle(LastDir, FakeTitle, word, '.mei', ChangeDir)
                            ChangeSongTitle(LastDir, FakeTitle, word, '.txt', ChangeDir)
                            ChangeDir = False # only change the last file of the last dir
                        FakeTitle = blank[ptr+1:-2]

                        #print (blank)
                        print(blank, file=fsong)
                        mark=4 # write individual song
                        continue
