import os
import pandas as pd
import numpy as np

def preprocessing() :
    '''
    Reading and cleaning the data. 
    
        Returns: 
            sorted(DataFrame): dataframe after preprocessing
    '''
    
    #read the dataset chocolate which we use for the whole project
    df = pd.read_csv("data/chocolate.csv", index_col = 0)

    #"_" replaced by a whitespace
    df.columns = df.columns.str.replace("[_]", " ", regex=True)
    #for all values 
    df = df.replace({"_":" "}, regex = True)
    
    #rename the values of column "vanilla"
    df = df.replace({"vanila":"vanilla"}, regex = True)
  

    #delete unused columns
    df.drop(columns=["ref", "fourth taste", "specific bean origin or bar name"], inplace = True, axis = 1)

    #fill NaN values for columns where we do not want to loose information else delete the columns with NaN values
    df["third taste"] = df["third taste"].fillna("no information")
    df["second taste"] = df["second taste"].fillna("no information")

     #sort data by rating in ascending orders
    sorted = df.sort_values(by=["rating"], ascending = False)

    #renumber index to start with 0
    sorted = sorted.reset_index()
  
   

    return sorted


def statistics():
    '''
    get the most important statistics for specific columns: mean, standard deviation, minimum value, maximum value, p% below the given values
        
        Returns: 
            df(DataFrame): summary statistics
    '''
    #description that is printed to describe what the user sees
    description_stat = "Description statistics: For the statistics we get the mean value, the standard deviation, the minimum and maximum value. 25%, 50%, 75% - the values stated in these rows describe that p% are below that given value. "
    #get the preprocessed data
    df = preprocessing()
    #get the columns for which we will see the statistics
    df = df[["cocoa percent", "rating", "counts of ingredients"]]
    print(description_stat + "\n")
    return df.describe()[1:]



def get_list_company():
    '''
    Returns name of all companies used in the dataset
        Returns: 
            companies(set): set with names of all companiew
    '''
    #description that is printed to describe what the user sees
    description_company= "Description get_list_company: Here you see a list with all companies that exist in the dataset."
    df = preprocessing()
    companies = set(df["company"])
    print(description_company + "\n")
    return companies

def get_list_country():
    '''
    Returns name of all countries used in the dataset
        Returns: 
            countries(set): set with names of all countries
    '''
    #description that is printed to describe what the user sees
    description_country= "Description get_list_country: Here you see a list with all countries that exist in the dataset."
    #get the preprocessed data
    df = preprocessing()
    #set of countries
    countries = set(df["company location"])
    print(description_country + "\n")
    return countries