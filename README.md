# Andrew Hughes Chant

Andrew Hughes. Canadian musicologist, born in London 3 Aug 1937; MA (Oxford) 1964, Ph.D. (Oxford) 1964. An authority on medieval liturgy and music. More of his information is available [here](http://www.thecanadianencyclopedia.ca/en/article/andrew-hughes-emc/).

In his research career, he published "Late Medieval Liturgical Offices (LMLO)", which contained more than 200 late medieval church feasts, and more than 5000 chant melodies.

Now, all chant melodies are available, which can be represented as musical scores for music theoretic, musicological and academic usage. The work was presented at the Music Encoding Conference, 2018. You can view the slides [here](https://drive.google.com/file/d/1-BKGfBQlGWAk_PXHPZeUyAUCjHvKH3Gv/view?usp=sharing). 

In this page, you will learn:

* How these chant melodies are organized hierarchically.
* How to view a single chant melody as musical score.
* How to download all chant melodies and save them locally.

# Chant Hierarchy

(1) All chant melodies are organized by saints' names alphabetically. You can view the complete list [here](https://github.com/DDMAL/Andrew-Hughes-Chant/tree/master/file_structure_text_file_MEI_file).

(2) Under each folder, you can see a list of saints' name belonging to that alphabet, where each of them presents an office. For example, see all the offices available for the saints' name beginning with [A](https://github.com/DDMAL/Andrew-Hughes-Chant/tree/master/file_structure_text_file_MEI_file/CH-A).

(3) Under the office folder (e.g., office for [Adalardus](https://github.com/DDMAL/Andrew-Hughes-Chant/tree/master/file_structure_text_file_MEI_file/CH-A/ADALARDUS/AD00)), you can see folders for all services. Often, they are `Vespers`, `Matins`, `Lauds` and `2nd Vespers`.

(4) Under the service folder (e.g., service for [Adalardus' 2nd Vesper](https://github.com/DDMAL/Andrew-Hughes-Chant/tree/master/file_structure_text_file_MEI_file/CH-A/ADALARDUS/AD00/2nd_Vespers)), you will see a list of chant melodies in MEI format, which will have the extension as `.mei` at the end of the file name. You can also see the same chant name with the extension as `.txt`, please IGNORE this file, and all you need is the `.mei` version of the chant.

Note: However, when you click on a chant melody file (e.g., [`O virum nobilem` of Adalardus' 2nd Vesper](https://github.com/DDMAL/Andrew-Hughes-Chant/blob/master/file_structure_text_file_MEI_file/CH-A/ADALARDUS/AD00/2nd_Vespers/O_virum_nobilem.mei)), you will see a hugh chunk of codes, rather than a musical score. Don't worry! The next section will show you how to turn the obscure codes into a readable musical score.

# How to View A Single Chant Melody as Musical Score?
From the section above, I hope you already know how to navigate through all chant melodies and find a chant melody you want. In this section, you will know how to render a musical score from the codes of a chant melody.

Take [`O virum nobilem` of Adalardus' 2nd Vesper](https://github.com/DDMAL/Andrew-Hughes-Chant/blob/master/file_structure_text_file_MEI_file/CH-A/ADALARDUS/AD00/2nd_Vespers/O_virum_nobilem.mei) as an example. In this page, you will see a navigation bar right above the code section, which looks like this:

![image](https://user-images.githubusercontent.com/9313094/43724687-99eeefe6-9968-11e8-984e-9f3c834ac305.png)

Click on the `Raw` button and you will see this [page](https://raw.githubusercontent.com/DDMAL/Andrew-Hughes-Chant/master/file_structure_text_file_MEI_file/CH-A/ADALARDUS/AD00/2nd_Vespers/O_virum_nobilem.mei). Within this page, select all the text (For Windows and Linux users, please use `ctrl + a`; Mac OS users, please user `command + a`) and copy it (For Windows and Linux users, please use `ctrl + c`; Mac OS users, please user `command + c`). Afterward, go to the musical score rendering website called [VerovioHumdrumViewer](https://verovio.humdrum.org/), which contain two sections: the code section on the left and the musical score section on the right:

![image](https://user-images.githubusercontent.com/9313094/43725143-b67bc19c-9969-11e8-9f01-d85dd495fe9f.png)


Please click on the left section, select all the text (For Windows and Linux users, please use `ctrl + a`; Mac OS users, please user `command + a`) and paste the text (For Windows and Linux users, please use `ctrl + v`; Mac OS users, please user `command + v`) you copied from `O virum nobilem` chant, then the left section will display the codes you copied from `O virum nobilem`, and the right section will display the musical score you want:

![image](https://user-images.githubusercontent.com/9313094/43725388-625865ce-996a-11e8-86e1-0d978b875919.png)

You can play the chant melody using the play button on the upper right corner.

Note: As you can see in this score, ```Plica``` is represented as ```grace note```, and ```Ligature``` is represented as ```slur```.  Also, to indicate a sentence, the first letter is capitalized. The last letter of a word being capitalized indicates rhyme.

# How to Download All Chant Melodies and Save Them Locally?

Although locating a chant melody online is explained above, what if you want to save all the chant melodies on your own computer? In this way, you can go into the chant diretory and __search__ a saint's name, or the title of a chant, or just simply access these chant melodies when you don't have Internet. To do this, simply download this [file](https://www.dropbox.com/s/xjkz7j114oqd6l4/Andrew_Hughes_Chant_MEI.zip?dl=0), which contains all the chant melodies. This file is a `zip` file, so you need to unzip it first, and within the folder, the file structure is EXACTLY the same with the one online, so you can navigate the same way as above to find any chant melody you want and render it as a musical score.

# Questions?

Hope the information above helps you to access all the chants as musical scores! If you have any question or suggestion, please send us an email to yaolong.ju@mail.mcgill.ca, and we will be glad to help you!
