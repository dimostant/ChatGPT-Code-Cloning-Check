from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

def compare_questions(api_question, gpt_question):
      
    print("comparing : " + api_question + " and " + gpt_question)
    
    X_list = word_tokenize(api_question)
    Y_list = word_tokenize(gpt_question)

    sw = stopwords.words('english')
    l1 =[];l2 =[]

    X_set ={w for w in X_list if not w in sw}
    Y_set ={w for w in Y_list if not w in sw}

    rvector= X_set.union(Y_set)

    for w in rvector:
        if w in X_set: l1.append(1)
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]

    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    print("similarity: ", cosine) 

    return cosine