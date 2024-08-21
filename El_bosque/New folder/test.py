import numpy as np 
import pandas as pd 


def change_num(number_options, number_questions):
    abc = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    options =  [abc[i] for i in range(number_options)]

    return options



def creation_test(number_questions, number_options, options):
    df = { i+1:[ 'O' for _ in range(number_options)] for i in range(number_questions)}
    df = pd.DataFrame(df)
    options = change_num(number_options, number_questions)
    df.index = options
    return df


def df_show(num_options, num_questions):
    num_options_list = ['' for i in range(num_options)]
    num_questions_list = [1+i for i in range(num_options)]

    df = {
        'P R E G U N T A': num_questions_list,
        'R E S P U E S T A ': num_options_list
        }
    
    df = pd.DataFrame(df)
    df = df.transpose()
    # df = df.to_csv('df.csv', header=False)
    return df
#a