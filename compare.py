from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

def compare_questions(api_question, gpt_question):
      
    print("comparing : " + api_question + " and " + gpt_question)
    
    x_list = word_tokenize(api_question)
    y_list = word_tokenize(gpt_question)

    sw = stopwords.words('english')
    l1 =[];l2 =[]

    x_set ={w for w in x_list if not w in sw}
    y_set ={w for w in y_list if not w in sw}

    r_vector= x_set.union(y_set)

    for w in r_vector:
        if w in x_set: l1.append(1)
        else: l1.append(0)
        if w in y_set: l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(r_vector)):
            c+= l1[i]*l2[i]

    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    print("similarity: ", cosine) 

    return cosine