import random
import csv
import sys
import json

###################################################

filename = open('Labels.csv', 'r')
 
file = csv.DictReader(filename)

######################
# options to get different data
debug_check = False

mistake_check = True

modified_sentence = False 

extra_sentence = True

occurrence = False

label_name = True
######################
# list set for different labels and read all data file
data_length_r =[]
gender_r = []
gender_t_r = []
race_r = []
color_r = []
hair_color_r = []
hair_length_r = []
hair_style_r = []
top_r = []
bot_r = []
shoes_r = []
acc_r = []
acc_t1_r = []
extras_f_r = []
extras_b_r = []
gender_real_r = []

with open('Labels.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for col in file:
        data_length_r.append(col['Data Length'])
        gender_r.append(col['Gender'])
        gender_t_r.append(col['Gender(third person)'])
        race_r.append(col['Race'])
        color_r.append(col['Color'])
        hair_color_r.append(col['Hair Color'])
        hair_length_r.append(col['Hair Length'])
        hair_style_r.append(col['Hair Style'])
        top_r.append(col['Top'])
        bot_r.append(col['Bottom'])
        shoes_r.append(col['Shoes'])
        acc_r.append(col['Accessory'])
        acc_t1_r.append(col['Accessory Action'])
        extras_f_r.append(col['Extra sentences F'])
        extras_b_r.append(col['Extra sentences B'])
        gender_real_r.append(col['Gender real'])

data_length_t = list(filter(None, data_length_r))
data_length = int(data_length_t[0])


gender = list(filter(None, gender_r))
gender_t = list(filter(None, gender_t_r))
gender_real = list(filter(None, gender_real_r))
gender1 = dict(zip(gender, gender_t))
gender2 = dict(zip(gender, gender_real))

race = list(filter(None, race_r))
color = list(filter(None, color_r))
hair_color = list(filter(None, hair_color_r))
hair_length = list(filter(None, hair_length_r))
hair_style = list(filter(None, hair_style_r))

top = list(filter(None, top_r))
bot = list(filter(None, bot_r))
shoes = list(filter(None, shoes_r))

acc = list(filter(None, acc_r))
acc_t1 = list(filter(None, acc_t1_r))
acc1 = dict(zip(acc, acc_t1))



###################################################
# options list
action = ["is wearing", "wears", "weared", "has", "had", "in", "with"]

choice = [0,1,2,3,4]
choice2 = [0,1,2]


###################################################
# extra sentence
if (modified_sentence):
    with open('f.txt') as ff:
        linesf = [line.rstrip('\n') for line in ff]

    with open('m.txt') as fm:
        linesm = [line.rstrip('\n') for line in fm]

    with open('f.txt') as fb:
        linesb = [line.rstrip('\n') for line in fb]
else:
    with open('Sentence_f.txt') as ff:
        linesf = [line.rstrip('\n') for line in ff]

    with open('Sentence_m.txt') as fm:
        linesm = [line.rstrip('\n') for line in fm]

    with open('Sentence_f.txt') as fb:
        linesb = [line.rstrip('\n') for line in fb]


with open('lt.txt') as flt:
    lineslt = [line.rstrip('\n') for line in flt]


extras_f = list(filter(None, extras_f_r)) + linesf + lineslt
extras_m = linesm + lineslt
extras_b = list(filter(None, extras_b_r)) + linesb + lineslt


###################################################
if debug_check:
    data_length = 2

# gender = ["male", "female", "man", "woman", "NA"]
# gender1 = {"male":"He", "female":"She", "man":"He", "woman":"She", "NA":"The person"}
# "boy", "girl"
# race = ["white", "black", "asian", "NA"]

# White.Black or African American.Asian.American Indian or Alaska Native.Native Hawaiian or Pacific Islander.
# color = ["red", "orange", "yellow", "green", "blue", "violet", "black", "white", "gold", "silver", "pink", "NA"]
# hair_color = ["black", "white", "gold", "silver", "NA"]
# hair_length = ["short", "long", "middle", "NA"]
# hair_style = ["NA"]
# top = ["suit", "shirt", "dress", "blouse", "tanktop", "coat", "jacket", "T-shirt", "jumper", "pullover", "cardigan", "sweatshirt", "NA"]
# bot = ["skirt", "trousers", "jeans", "shorts", "NA"]
# shoes = ["shoes", "sandals", "boots", "wellingtons", "slippers", "NA"]
# acc = ["hat", "belt", "handbag", "glasses", "headscarf", "scarf", "sunglasses", "gloves", "bracelet", "necklace", "ring", "earrings", "NA"]
# acc1 = {"hat":"is wearing a", "belt":"has", "handbag":"carries", "glasses":"is wearing a pair of", "headscarf":"is wear a", "scarf":"is wear a", "sunglasses":"is wearing a pair of", "gloves":"is wearing a pair of", "bracelet":"is wearing a", "necklace":"is wearing a", "ring":"has a", "earrings":"is wearing ", "NA":""}

###################################################
# options list
sentence = []
label = []
label2 = []
sentence_format = ['1','2','3','4','5','6']




###################################################
# pair and group relative labels
def pair_race_gender(race, gender):
    ch = random.choice(choice)
    if race == "NA":
        return gender
    else:
        if(ch == 0):
            racegender = gender + " with the appearance of " + race
        else:
            racegender = race + " " + gender
            
        return racegender

def group_hair_cls(length, color, style):
    temp_h = ""
    if (color == "NA" and length == "NA" and style == "NA"):
        return ""
    elif (color == "NA" and length == "NA"):
        return style
    elif (style == "NA" and length == "NA"):
        return color
    elif (style == "NA" and color == "NA"):
        return length
    elif (color == "NA" ):
        hair_ls = length + " " + style
        return hair_ls
    elif (length == "NA"):
        hair_cs = color + " " + style
        return hair_cs
    elif (style == "NA"):
        hair_lc = length + " " + color
        return hair_lc
    else:
        hair_lcs = length + " " + color + " " + style
        return hair_lcs

def pair_cs(color, style):
    ch = random.choice(choice)
    if style == "NA":
        return ""
    elif (color == "NA"):
        return style
    else:
        if(ch == 0):
            cs = style + " with the color " + color
        else:
            cs = color + " " + style
            
        return cs
    


def group_top_bottom_shoes(top, bot, shoes):
    clothes = []

    clothes_temp = ""
    temp2 = ["a ", ""]
    temp3 = ""
    if top != "":
        clothes.append(top)
        temp3 = temp3 + random.choice(temp2)
        if (top == ""):
            temp3 = ""   
    
    if bot != "":
        clothes.append(bot)
    if shoes != "":   
        clothes.append(shoes)
    
    
    if len(clothes) == 3:
        clothes_temp = temp3 + clothes[0] + ", " + clothes[1] + " and "  + clothes[2]
    if len(clothes) == 2:
        clothes_temp = temp3 + clothes[0] + " and " + clothes[1]
    if len(clothes) == 1:
        clothes_temp = temp3 + clothes[0]

    return clothes_temp

#########################################################################################################################################################
# generator 6 type of sentences
def sentence_generator(race_gender, hair, top, bot, shoes, acc_cs, gender, acc, race):
    
    format_t = random.choice(sentence_format)

    action_t = random.choice(action)

    ch = random.choice(choice2)
    ms = ""
    if (extra_sentence):
        if(ch == 0):
            ms = ""
        else:
            ms = " " + random.choice(extras_m)
    


    

    temp1 = ["The", "A", "This", "That"]
    hair_d = ""
    acc_temp = ""

    if format_t == '1':
        
        temp1_1 = random.choice(temp1)
        if (temp1_1 == "A" and race_gender[0] == "A"):
            temp1_1 = "An"

        
        if (hair != ""):
            hair_d = " with " + hair + " hair,"
        
        clothes_temp = group_top_bottom_shoes(top, bot, shoes) 
        
        acc_temp = ""
        if acc_cs == "":
            acc_temp = ""
        else:
            acc_temp = ", who " + acc1[acc] + " "

        sentence_temp = temp1_1 + " " + race_gender + hair_d + " " + action_t + " " + clothes_temp + acc_temp + acc_cs + "."
        return sentence_temp

    if format_t == '2':
        temp1 = ["The", "A"]
        temp1_1 = random.choice(temp1)
        if (temp1_1 == "A" and race_gender[0] == "A"):
            temp1_1 = "An"
        
        hair_d = ""
        if (hair != ""):
            hair_d = ", has " + hair + " hair"
        
        clothes_temp = group_top_bottom_shoes(top, bot, shoes) 
        
        acc_temp = ""
        if acc_cs == "":
            acc_temp = ""
        else:
            acc_temp = "." + ms + " " + "The person also " + acc1[acc] + " " + acc_cs
            
        sentence_temp = temp1_1 + " " +race_gender + " " + action_t + " " + clothes_temp + hair_d + acc_temp + "."
        return sentence_temp

    if format_t == '3':
        temp1 = ["The", "A"]
        temp1_1 = random.choice(temp1)
        if (temp1_1 == "A" and race_gender[0] == "A"):
            temp1_1 = "An"

        if (hair != ""):
            hair_d = " has " + hair + " hair"
        
        clothes_temp = group_top_bottom_shoes(top, bot, shoes)       

        if acc_cs == "":
            acc_temp = ""
        else:
            acc_temp = "." + ms + " " + gender1[gender] + " " + acc1[acc] + " "

           
        sentence_temp = temp1_1 + " " + race_gender + hair_d + ". " + gender1[gender] + " " + action_t + " " + clothes_temp + acc_temp + acc_cs + "."
        return sentence_temp
    
    if format_t == '4':

        temp1_1 = random.choice(temp1)
        if (temp1_1 == "A" and gender[0] == "A"):
            temp1_1 = "An"

        gender_t = gender
        if (gender == "NA"):
            gender_t = "person"

        if (hair != ""):
            hair_d = ", that has " + hair + " hair"
        
        clothes_temp = group_top_bottom_shoes(top, bot, shoes) 
        
        if acc_cs == "":
            acc_temp = ""
        else:
            acc_temp = "." + ms + " " + gender1[gender] + " " + acc1[acc] + " "

        race_temp = ","
        if (race != "NA"):
            race_temp = " described as " + race + ","

            
        sentence_temp = temp1_1 + " " + gender_t + race_temp + " " + action_t + " " + clothes_temp + hair_d + acc_temp + acc_cs + "."
        return sentence_temp

    if format_t == '5':

        temp1_1 = random.choice(temp1)
        if (temp1_1 == "A" and gender[0] == "A"):
            temp1_1 = "An"

        
        clothes_temp = group_top_bottom_shoes(top, bot, shoes) 


        if (hair != ""):
            hair_d = hair + " hair, "

        if acc_cs == "":
            acc_temp = ""
        else:
            acc_temp = ", " +  acc1[acc] + " " + acc_cs

            
        sentence_temp = temp1_1 + " " + race_gender + ", " + hair_d  + clothes_temp + acc_temp + "."
        return sentence_temp
    
    if format_t == '6':

        temp1_1 = random.choice(temp1)
        if (temp1_1 == "A" and gender[0] == "A"):
            temp1_1 = "An"

        
        clothes_temp = group_top_bottom_shoes(top, bot, shoes) 


        if (hair != ""):
            hair_d = ", with " + hair + " hair"

        if acc_cs == "":
            acc_temp = ""
        else:
            acc_temp = ", " +  acc1[acc] + " " + acc_cs

            
        sentence_temp = temp1_1 + " " + race_gender + acc_temp + ", "   + clothes_temp + hair_d + "."
        return sentence_temp

    else:
        return ""


 # extra sentences added
def extra_sentences(sentence):
    sf = ""
    sb = ""
    sfc = random.choice(choice2)
    sbc = random.choice(choice2)

    if (sfc != 0):
        sf = random.choice(extras_f) + " "
    if (sbc != 0):
        sb = " " + random.choice(extras_b)
    final_sentence = sf + sentence + sb
    return final_sentence

def Convert(label_list):
    zero_list = [0] * len(label_list)
    label_dict = dict(zip(label_list, zero_list))
    return label_dict


#########################################################################################################################################################
# frequency function
labels3 = {"race":{}, "gender":{}, "hair_style":{}, "hair_color":{}, "hair_len":{}, "top":{}, "top_color":{}, "bottom":{}, "bottom_color":{}, "footwear":{}, "footwear_color":{}, "accessory":{}, "accessory_color":{}}

race_l =Convert(race)
gender_l = Convert(gender)
hair_style_l = Convert(hair_style)
hair_color_l = Convert(hair_color)
hair_len_l = Convert(hair_length)
top_l = Convert(top)
top_color_l = Convert(color)
bottom_l = Convert(bot)
bottom_color_l = Convert(color)
footwear_l = Convert(shoes)
footwear_color_l = Convert(color)
accessory_l = Convert(acc)
accessory_color_l = Convert(color)




#########################################################################################################################################################
# generate data one by one




for i in range(data_length):
    labels = {"text":"", "race":"", "gender":"", "hair_style":"", "hair_color":"", "hair_len":"", "top":"", "top_color":"", "bottom":"", "bottom_color":"", "footwear":"", "footwear_color":"", "accessory":"", "accessory_color":""}
    labels2 = {"race":"", "gender":"", "hair_style":"", "hair_color":"", "hair_len":"", "top":"", "top_color":"", "bottom":"", "bottom_color":"", "footwear":"", "footwear_color":"", "accessory":"", "accessory_color":""}
    labels4 = {"text":"", "race":"", "gender":"", "hair_style":"", "hair_color":"", "hair_len":"", "top":"", "top_color":"", "bottom":"", "bottom_color":"", "footwear":"", "footwear_color":"", "accessory":"", "accessory_color":""}

    race_r = ""
    gender_r = ""
    hair_l = ""
    hair_c = ""
    hair_s = ""
    top_c = ""
    top_s = ""
    bot_c = ""
    bot_s = ""
    shoes_c = ""
    shoes_s = ""
    acc_c = ""
    acc_s = ""

    ##################################

    race_r = random.choice(race)
    labels["race"] = race_r
    labels2["race"] = race_r

    race_l[race_r] += 1

    ##################################
    gender_r = random.choice(gender)
    labels["gender"] = gender2[gender_r]
    labels2["gender"] = gender2[gender_r]
    gender_l[gender_r] += 1


    if gender_r == "NA":
        gender_r = "person"
    race_gender = pair_race_gender(race_r, gender_r)
    if gender_r == "person":
        gender_r = "NA"

    ##################################

    hair_l = random.choice(hair_length) 
    hair_c = random.choice(hair_color) 
    hair_s = random.choice(hair_style)  
    labels["hair_len"] = hair_l
    labels["hair_color"] = hair_c
    labels["hair_style"] = hair_s
    labels2["hair_len"] = hair_l
    labels2["hair_color"] = hair_c
    labels2["hair_style"] = hair_s

    hair_style_l[hair_s] += 1
    hair_color_l[hair_c] += 1
    hair_len_l[hair_l] += 1

    hair_lcs = group_hair_cls(hair_l, hair_c, hair_s)

    ##################################

    top_c = random.choice(color)
    top_s = random.choice(top)
    if top_s == "NA":
        top_c = "NA"
    labels["top_color"] = top_c
    labels["top"] = top_s
    labels2["top_color"] = top_c
    labels2["top"] = top_s

    top_l[top_s] += 1
    top_color_l[top_c] += 1

    top_cs = pair_cs(top_c, top_s)

    ##################################

    bot_c = random.choice(color)
    bot_s = random.choice(bot)
    if bot_s == "NA":
        bot_c = "NA"
    labels["bottom_color"] = bot_c
    labels["bottom"] = bot_s
    labels2["bottom_color"] = bot_c
    labels2["bottom"] = bot_s

    bottom_l[bot_s] += 1
    bottom_color_l[bot_c] += 1

    bot_cs = pair_cs(bot_c, bot_s)

    ##################################

    shoes_c = random.choice(color)
    shoes_s = random.choice(shoes)
    if shoes_s == "NA":
        shoes_c = "NA"

    labels["footwear_color"] = shoes_c
    labels["footwear"] = shoes_s
    labels2["footwear_color"] = shoes_c
    labels2["footwear"] = shoes_s

    footwear_l[shoes_s] += 1
    footwear_color_l[shoes_c] += 1

    shoes_cs = pair_cs(shoes_c, shoes_s)

    ##################################


    acc_c = random.choice(color)
    acc_s = random.choice(acc)

    if acc_s == "NA":
        acc_c = "NA"
    labels["accessory_color"] = acc_c
    labels["accessory"] = acc_s
    labels2["accessory_color"] = acc_c
    labels2["accessory"] = acc_s

    accessory_l[acc_s] += 1
    accessory_color_l[acc_c] += 1

    acc_cs = pair_cs(acc_c, acc_s)
    


    ###################################################################


    sentence_t = sentence_generator(race_gender, hair_lcs, top_cs, bot_cs, shoes_cs, acc_cs, gender_r, acc_s, race_r)


    if(extra_sentence):
        sentence_f = extra_sentences(sentence_t)
    else:
        sentence_f = sentence_t

    sentence.append(sentence_f)
    labels["text"] = sentence_f
    label.append(labels)
    label2.append(labels2)

    # if(debug_check == True):

    #     print(labels)
    #     print("_____________________")
    #     print(labels2)
    #     print("+++++++++++++++++++++++++++++++++++++++++")
    #     print(label)
    #     print("_____________________")
    #     print(label2)
    #     print("=========================================")

    
# if(debug_check == True):
#     print("----")
#     print(label)
#     print("----")

for i in range(data_length):

#########################################################################################################################################################
    if(debug_check == True):
        print(sentence[i])
        print(label[i])
        print("_____________________")
        print(label2[i])
        print("########################################")


#########################################################################################################################################################

labels3["race"].update(race_l)
labels3["gender"].update(gender_l)
labels3["hair_style"].update(hair_style_l)
labels3["hair_color"].update(hair_color_l)
labels3["hair_len"].update(hair_len_l)
labels3["top"].update(top_l)
labels3["top_color"].update(top_color_l)
labels3["bottom"].update(bottom_l)
labels3["bottom_color"].update(bottom_color_l)
labels3["footwear"].update(footwear_l)
labels3["footwear_color"].update(footwear_color_l)
labels3["accessory"].update(accessory_l)
labels3["accessory_color"].update(accessory_color_l)

# fake_temp = label[567]
# fake_temp["footwear"] = "NA"
# fake_temp["footwear_color"]="red"

if(mistake_check):
    print("Mistake Checked") 
    for i in range(data_length):
        mistake_temp = label[i]
        if (mistake_temp["footwear"] == "NA" and mistake_temp["footwear_color"]!="NA"):
            print("Something wrong")
        if (mistake_temp["accessory"] == "NA" and mistake_temp["accessory_color"]!="NA"):
            print(i)
            print("Something wrong")



#########################################################################################################################################################
name = ""
patterns = len(sentence_format)
cat = len(labels2)
maxsubcat = [len(gender), len(race), len(color), len(hair_color), len(hair_length), len(hair_style), len(top), len(bot), len(shoes), len(acc)]
subcat = max(maxsubcat)
name = "partern" + str(patterns) + "cat" + str(cat) + "subcat" + str(subcat)
# print(name)
#########################################################################################################################################################

name1 = name + "(detail).csv"
name2 = name + ".json"
name3 = name + "(occurrence).json"
name4 = name + ".csv"

# return the results to suitable files


if(debug_check == False):
    result = []
    for i in range(data_length):
        result_temp = []
        result_temp.append(sentence[i])
        result_temp.append(label2[i])
        result.append(result_temp)

    fields = ['Sentence', 'Labels'] 
    if(label_name == False):
        name1 = 'data.csv'
    
    with open(name1, 'w') as f:
    # with open(str(sys.argv[-1]), 'w') as f:
        write = csv.writer(f)  
        write.writerow(fields)
        write.writerows(result)



#########################################################################################################################################################
    result2 = []
    for i in range(data_length):
        result2.append(label[i])


    j = json.dumps(result2, indent = 2)
    if(label_name == False):
        name2 = 'data.json'
    f2 = open(name2,'w')
    print(j, file = f2)



#########################################################################################################################################################
    result4 = []
    for i in range(data_length):

        result_temp4 = []
        result_temp4f = []
        result_temp4.append(sentence[i])
        temp_sub = label2[i]
        list_sub = list(temp_sub.values())
        result_temp4s = result_temp4 + list_sub    
        result_temp4f.append(str(result_temp4s))
        result_temp4f.append("")
        result4.append(result_temp4f)

    fields2 = ['Sentence', ''] 
    if(label_name == False):
        name4 = 'data2.csv'
    with open(name4, 'w') as f:

        write = csv.writer(f)  
        write.writerow(fields2)
        write.writerows(result4)


#########################################################################################################################################################







    


if(occurrence):
    print("###################################################################")
    print(labels3)


#########################################################################################################################################################
if(debug_check == False):
    result3 = []
    result3.append(labels3)


    j = json.dumps(result3, indent = 2)
    if(label_name == False):
        name3 = 'occurrence.json'
    f3 = open(name3,'w')
    print(j, file = f3)

print("###################################################################")


print("Data generation done, check data.csv")


print("###################################################################")




# The difficulties:
# 1. narration = True/False, text contains sentences that is not description of the suspects
# 2. patterns = no. of ways of description
# 3. categories = num_of_appearance_catagories=5, #eg [gender,race,top,bottom,shoes]
# 4. classses = for each of the catagories above. eg [na,male,female],[na,caucasian,black,asian],[t-shirt]


# Solution:
# 1. narration = extra_sentence = False
# 2. patterns = 5; sentence_format = ['1','2','3','4','5']
# 3. categories; len(labels2) = 13
# 4. classses; len(gender) = 4

# text,race,gender,hair_style,hair_color,hair_len,short,
# 'An Asian female has short white wavy hair. She in a blue jacket, red jeans and white slippers. She is wearing a red bracelet.', 'Asian', 'female', 'wavy', 'white', 'short'

