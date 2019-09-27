# Samuel Scalise
# Undergraduate
# Python
# Project 1 Machine Learning
# Naive Bayes
# Need Python standard add-on csv(comes with every installation of Python >= 2.7)
#   CSV is just the standard comma separated format for text files
# Summary:
#       This program run and classify a naive bayes algorithm on any binary classification with binary keyword based
#       attributes in CSV format. The program will then predict the classification of input sentences based on the
#       training set.
import csv

title = []
rows = []
training = input("training set file:\n")
# Open training set data in csv format and fill in a list for column titles and fill in a list of lists for row data
# Keep track of the number of rows and the number of columns
with open(training) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            for item in row:
                title.append(item)
        else:
            rows.append(row)
            line_count += 1
    row_count = line_count - 1
    column_count = 0
    for i in title:
        column_count += 1

    # Create lists to keep the number of instances of each case per column:
    #   the word exists and the sentence is cs related
    #   the word exists in the sentence and is not cs related
    #   the word does not exist and the sentence is cs related
    #   the word does not exist and the sentence is not cs related
    column_exist_cs = []
    column_exist_ncs = []
    column_dexist_cs = []
    column_dexist_ncs = []

    # Fill each of these lists with a '0' value for each column
    for i in range(0, column_count):
        column_exist_cs.append(0)
        column_exist_ncs.append(0)
        column_dexist_cs.append(0)
        column_dexist_ncs.append(0)

    # Next go through each row and tally the results in the appropriate list
    for row in rows:
        position = 0
        for item in row:
            if item == '1':
                if row[column_count - 1] == '1':
                    column_exist_cs[position] += 1
                else:
                    column_exist_ncs[position] += 1
            else:
                if row[column_count - 1] == '1':
                    column_dexist_cs[position] += 1
                else:
                    column_dexist_ncs[position] += 1
            position += 1

# Now find the likelyhood for class yes and class no for later
# Also find number of total cs and total non cs
p_y = 0
p_n = 0
cs = 0
ncs = 0
for row in rows:
    if row[column_count - 1] == '1':
        p_y += 1
        cs += 1
p_y = p_y / row_count
p_n = 1 - p_y
ncs = row_count - cs

# Now remove the nonsense values for the classification row (the last row from the training set)
column_exist_cs.pop()
column_exist_ncs.pop()
column_dexist_cs.pop()
column_dexist_ncs.pop()

# Now find the likelyhood of each attribute given the class
#   Creates four lists: p(1|1),p(0|1), p(1|0), p(0|0)
# will include smoothing at this point
#   smoothing is add 1 to the numerator and add 2 to the denominator because the attributes are all binary
p_exist_cs = []
p_dexist_cs = []
p_exist_ncs = []
p_dexist_ncs = []

for pos in range(0, column_count - 1):
    p_exist_cs.append((column_exist_cs[pos] + 1)/(cs + 2))
    p_dexist_cs.append((column_dexist_cs[pos] + 1)/(cs + 2))
    p_exist_ncs.append((column_exist_ncs[pos] + 1)/(ncs + 2))
    p_dexist_ncs.append((column_dexist_ncs[pos] + 1)/(ncs + 2))

# Now take input sentences
# In this case we are using input1.txt
sentences = []
sentence_count = 0
inf = input("input file:\n")
with open(inf, 'r') as f:
    for line in f:
        sentences.append(line)
        sentence_count += 1

# Now manipulate each sentence until they are split into lower case keywords
clean_sentences = []
for line in sentences:
    temp = line.lower()
    temp = temp.replace('.', '')
    temp = temp.replace('!', '')
    temp = temp.replace('?', '')
    temp = temp.replace(',', '')
    temp = temp.strip('\n')
    temp = temp.replace('"', '')
    temp = temp.replace(':', '')
    temp = temp.replace(';', '')
    clean_sentences.append(temp)

# Now make list of lists for the tabular form of keywords within each sentence
sentence_keyword = []
for i in range(0, sentence_count):
    temp = []
    for a in range(1, column_count):
        temp.append(0)
    sentence_keyword.append(temp)

# Now match any keywords in each sentence and record them in sentence_keyword
for pos in range(0, sentence_count):
    temp_sentence = clean_sentences[pos].split(" ")
    for word in temp_sentence:
        for position in range(0, column_count - 1):
            if word == title[position]:
                sentence_keyword[pos][position] = 1

# Now create list for values in top half of bayes for classification: yes and no
classification_yes = []
classification_no = []

for pos in range(0, sentence_count):
    total_yes = 1
    total_no = 1
    for position in range(0, column_count - 1):
        if sentence_keyword[pos][position] == 1:
            total_yes *= p_exist_cs[position]
        else:
            total_yes *= p_dexist_cs[position]
        if sentence_keyword[pos][position] == 1:
            total_no *= p_exist_ncs[position]
        else:
            total_no *= p_dexist_ncs[position]
    total_yes *= p_y
    total_no *= p_n
    classification_yes.append(total_yes)
    classification_no.append(total_no)

# Now for each sentence check if classification yes or no is larger to get the predicted classification
# The formula has you divide by P(Each Attribute in the sentence) but it is the same for classification yes and no
# meaning that the answer will be proportional and will work to find which side is greater even without the division
classification_predict = []
for pos in range(0, sentence_count):
    if classification_yes[pos] > classification_no[pos]:
        classification_predict.append(1)
    else:
        classification_predict.append(0)

# Now make clean output file
with open("outputpr1.txt", "w") as f:
    count = 0
    for item in classification_predict:
        count += 1
        temp = "no"
        if item == 1:
            temp = "yes"
        f.write(f"sentence {count}:\t{temp}\n")
