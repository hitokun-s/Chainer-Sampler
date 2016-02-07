*************
* Lists.tgz *
*************

Copyright: Teo de Campos and Manik Varma (Microsoft Research)


The files in this directory tree contain information of the lists of
splits of sample sets used for training, validation and test of our
classification algorithms, as shown in the VISAPP09 paper.

All that really matters for the experiments in the Lists directory are
the MatLab files called "lists.mat" (or something similar). The other
files where used to build this MatLab structure. 
Please, contact me if you do not have access to MatLab, so that I will
do my best to generate ASCII version of the list datafiles.

I'll explain this using the English Images dataset as an example. This
list is at: 
<current directory>/Lists/English/Img/lists.mat

When you load "lists" in MatLab, you'll get this structure:

list = 

       ALLnames: [12503x34 char]
        is_good: [12503x1 logical]
      ALLlabels: [12503x1 uint16]
    classlabels: [62x1 double]
     classnames: [62x21 char]
     NUMclasses: 62
         TSTind: [930x16 uint16]
         VALind: [844x16 uint16]
         TXNind: [930x16 uint16]
         TRNind: [930x16 uint16]


The four last elements should dictate the experiments.
The experiments in the VISAPP paper show results with several random
splits of samples for training, validation and testing of the
methods. In the case of the English dataset, there are 16 splits
(obviously with no overlap between the train/test sets). So, the last
four elements above are lists of indexes for each split: each column
corresponds to a split, so the elements of a column list all the
sample images used in that split. More specifically: 

* list.TSTind: test 
* list.VALind: validation 
* list.TXNind: texton, i.e., elements used to learn the visual
	       vocabularies. We used all the training samples here, so
	       list.TXNind==list.TRNind 
* list.TRNind: training samples


This is how we built the splits:

(1) Fixed a TEST set with 15 samples per class, this is why the
    "lists.TSTind" has repeated columns. 
(2) Increased the TRAINING set from 5:2:15 (in MatLab notation). There
    are 3 splits of each size, except for the split of size 15, which
    is a single set, since some classes have only 30 samples in total.
(3) The validation set has a different number of samples per class
    (smaller than the training set) and some of its elements are in the
    training set. 

For instance, the very first training sample of the first split is the
file you get by doing this: 

>> list.ALLnames(list.TRNind(1,1),:)

ans =

GoodImg/Bmp/Sample001/img001-00038

So you just need to append the base directory to the above string and
the termination '.png' to the end of the above filename. In the case
of my local directory structure, this works by doing this: 

>> img = imread(['../../../Images/Originals/English/Img/', list.ALLnames(list.TRNind(1,1),:), '.png']);
>> image(img)

The above should show a pretty ugly "0" on the screen.

more generically, if you want to show a sequence of all the training
samples of split number one, you can do this: 

S=1;
for T=1:310, 
   img = imread(['../../../Images/Originals/English/Img/', list.ALLnames(list.TRNind(T,S),:),'.png']);image(img);
   pause(.1); 
end

You can do it for other splits (up to 16 in this case) and other sets (TST, VAL and TXT).

Now, to the other elements of list:
* list.is_good: this is an array of binary flags. In our splits, we only
  considered samples labeled as good (is_good==true).
* list.ALLlabels: this is the numeric label of each sample in
  ALLnames, it goes from 1 (which is the digit '0') to 62 (which is the
  character 'z') for English. 
* list.classlabel: list of distinct labels which occur in this
  dataset. In the case of English, this is a straightforward array from
  1 to 62. This is more interesting for Kannada, because we did not
  consider all the possible labels in our experiments. 
* list.classnames: just has the part of the filenames in ALLnames
  which tell which class the character belongs to. 
* list.NUMclasses: total number of classes in this dataset.




