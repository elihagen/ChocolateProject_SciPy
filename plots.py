import pandas as pd
import numpy as np
import seaborn as sns 
from matplotlib import pyplot as plt
import plotly.express as px
import ipywidgets as widgets



def review_dates(df):
    '''
    Histograms of when the reviews took place
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            rel(Axes): axes with plot for the years and number of reviews
    '''
    #description that is printed to describe what the user sees
    description = "review_dates \nDescription: The reviews took place between 2006 and 2020. Most of the surveys were conducted in 2015. In the years before and after, the number of surveys decreases quite steadily. However, after the year 2015 there was a stronger decrease and the lowest number of surveys was in 2020."

    #plot for review dates
    rel = sns.displot(df["review date"], kde=True)

    print(description)
    return rel


def ratings(df):
    '''
    Histograms showing the density per rating
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            rel(Axes): density of the ratings
    '''
    #description that is printed to describe what the user sees
    description= "ratings\nDescription: The ratings lie between 1.0 and 4.0 with 1.0 being unpleasant and 4.0 being 'premium' which the creators of the dataset describe as 'superior flavor development, character and style'. The mean value is around 3.2, which means that most chocolates are rated as rather tasty overall. Most chocolates are rated with 3.0 and 3.5 and least are rated with 2.0 and 2.25."
    
    #give the mean of all ratings rounded to 3 decimal places 
    s = "mean of ratings: " + str(round(np.mean(df["rating"]),3))

    #plot
    rel = sns.displot(df["rating"], kde=True)

    print(description)
    return rel
    


#function for getting the absolute values for each value of the pie chart
def func_absolute(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:d}".format(absolute)

def cocoa_percent(df):
    
    '''
      two subpplots showing the distribution of cocoa percent in the chocolates
        Parameters: 
          df(DataFrame): dateframe used for plotting
          Returns: 
            plt(Axes): distribution of the cocoa percent
            
    '''

    #description that is printed to describe what the user sees
    description = "cocoa_percent \nDescription: Here you can see that most chocolates have a cocoa content of 70-75%. There are very few chocolates below 65% and above 80%. These make up a share of less than 2% each and are exluded from the pie chart."
    #first plot is a histogram showing the counts for the individual chocoloate percentages
    plot1 = plt.figure(1)
    plt.hist(df["cocoa percent"])
    plt.xlabel("cocoa percent")
    plt.ylabel("counts")
    plt.title("cocoa percentage")

    #second plot is a piechart showing all percentages that make more than 2% of all chocolates
    plot2 = plt.figure(2)
    number = df["cocoa percent"].value_counts()
    number = number[number > df["cocoa percent"].count()*0.02]
    mylabel = number.index
    plt.pie(number, labels = mylabel, autopct=lambda pct: func_absolute(pct, number[number.index]))
    plt.title("counts of cocoa percentage that lie above 2%")
    print(description)
    plt.show()
    return plt
 

def cocoa_percent_rating(df):
    '''
    Box plot(interactive) showing the distribution of cocoa percent per rating. 
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            fig(Boxplot): inner quartiles of the cocoa percent per rating
    '''
    description = "cocoa_percent_rating \nDescription: A boxplot is shown for the cocoa percentage as a function of the ratings. For the rating 1, 1.75, and 2.6, there is only one data value, so only one line is shown here for this cocoa percentage. Let's take the 2.5 rating as an example. The maximum value is 100% and the minimum value is 55%. However, these values are outliers. All values below the lower fence and above the upper fence are considered outliers. The fences are 1.5 times the boxes with the median and quantile values we now come to. The median is 71%, which means that 71% is the value that divides all examples in half. The 1st quantile is 70%. 25% of all data points scoring 2.5 are below this quantile, 75% are above. 75% is the percentage of cocoa that makes up the 3rd quantile. Here it is exactly the opposite. 25% are above and 75% below this value. What we can see from this graph is that it does not depend on the cocoa content how the chocolate is rated. Most of the boxes are between 70% and 73%. For rating 1.5 it is different. Here the box ranges from 66% to 86%. Since this plot is interactive, you can move your mouse to any point and the values described will be displayed."

    #create the boxplot
    fig = px.box(df,x="rating", y="cocoa percent", title="rating ~ cocoa percent")

    print(description)
    return fig
    

def bean_origin_rating(df):
    '''
    Box plot showing the mean rating of the individual countries
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            ax(Axes): inner quartiles of the rating per country
    '''
    #description that is printed to describe what the user sees
    description = "bean_origin_rating \nDescription: Here we can see the how the different cocoa beans are rated depending on the country of bean origin. Most of the countries are very evenly distributed between 3.0 and 3.5. But we can see one country that is swinging upward. The chocolate with country of bean origin 'Solomon islands'(maybe also the one from Cuba) is rated better in average. The chocolate with bean origin from Puerto Rico is rated the worst. For these two we do not have outliers. This is the case for other countries. Blend, for example, (which is most likely a blend of beans from different countries) has a median of 3.0 but an outlier at 1.0 and 1.5 rating. Contrary, Uganda, where the median is lower at 2.75 but an outlier at 3.75 rating."
    df = df.sort_values(by='country of bean origin')
    rating = df["rating"]
    country = df["country of bean origin"]
    sns.set(rc = {'figure.figsize':(21,8)})
    #create the boxplot
    ax = sns.boxplot(x=country,y=rating)
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 85) 
    ax.set_title("country of bean origin ~ rating")
    print(description)
    return ax


def company_rating(df):
    '''
    Box plots(interactive) showing the rating per company
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            plot(Boxplot): inner quartiles of the rating per company
    '''
    #description that is printed to describe what the user sees
    description= "company_rating \nDescription: Below you can choose for which company (give the first letter of your company) you want to see the average rating. This will help you decide whether you really want to buy chocolate from the company or reconsider your decision. You should prefer companies whose interquartile range (the colored boxes) are further up. \nFYI: the interactive tool only works when you exit the input interface / stop running the cell! :("
    
    #options used for text box
    criteria_letter = widgets.Dropdown(
        options=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
        description= "First letter of company",
        disabled=False
    )
    

    def plot(criteria):
        '''
        Box plot showing the quartiles of rating per company. The user chooses which companies she wishes to see. 
            Parameters: 
                criteria: first letter of the company the user wishes to be displayed
        '''
        #dataframe with the desired companies
        new_df = df[df["company"].str.startswith(criteria)]
        #create boxplot
        ax = sns.boxplot(x = "company", y = "rating",data = new_df)
        ax.set_title("rating~company")
        ax.set_xticklabels(ax.get_xticklabels(),rotation = 85)
        


    print(description) 
    return widgets.interact(plot, criteria = criteria_letter)


def company_count(df):
    '''
    Bar chart(interactive) that visualizes how many companies exists per country 
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            fig(Barplot): counts of companies per location
    '''
    #description that is printed to describe what the user sees
    description = "company_count \nDescription: Most chocolate manufacturers come from the U.S.A with more than 800 companies. Three countries (Canada, France and the U.K.) have over 100 companies. All other countries have less than 100 companies and some even only one."
    #get the counts of companies per country
    df2 = df.groupby("company location")["company"].count().reset_index(name="count")
    #create a bar plot 
    fig = px.bar(df2, x= "company location", y = "count", title= "Companies per company location")
    print(description) 
    return fig



def companies(df):
    '''
    Treemap that visualizes the companies per country with their mean rating
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            rel(Figure): treemap with companies per country
    '''
    #description that is printed to describe what the user sees
    description = "companies \nDescription: At first glance, this tree diagram may look very confusing, but we will explain it to you in more detail so that you can extract a lot of information. The colours stand for the rating as shown in the legend on the right. The USA has the most companies with 984. Here the area shown is proportional to the number. Thus, the 6 companies that have 1 as their counted value are the smallest. All the companies in the USA are listed as children in the tree diagram. If you move the mouse over these companies (or over the country) you will see the number of chocolates produced, the average rating and the name of the company and the parent."

    #create the treemap that is to be colored(from red = bad to green = best) depending on the rating 
    fig = px.treemap(df, path=["company location", 'company'],color='rating',color_continuous_scale=["red", "green"])

    print(description) 
    return fig



def func(pct, allvals):
    '''
    used by plot_tastes to get the absolute values of the tastes
        Parameters: 
            pct: 
            allvals: tastes we want to display
        Returns: 
            absolute counts of the most common tastes
    '''
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def plot_tastes(df,taste,description):
    '''
    Pie chart with the 5 most common tastes. In the main program we choose for which taste we want to see the most common tastes
        Parameters: 
            df(DataFrame): dateframe used for plotting
            taste(String): name of the column we want the most common tastes from
            description(String): description of the Pie chart
        Returns: 
            plt(Pie chart): Pie chart with the 5 most common tastes
    '''
    #delete those columns with no information
    df2 = df[df[taste] != "no information"] 
    #count per values
    df2 = df2[taste].value_counts()
    #get the 5 most common tastes
    df2 = df2.head(5)
    #label of the tastes
    mylabels = df2.index[:5]
    #create pie chart
    plt.pie(df2, labels = mylabels, autopct=lambda pct: func(pct, df2))
    plt.title("Most " + taste + "s")
    print(description) 
    plt.show()
    return plt


def first_taste_years(df):
    '''
    counts of the first tastes per year that are rated 3.5 or higher
        Parameters: 
            df(DataFrame): dateframe used for plotting
        Returns: 
            fig(Scatterplot): scatter plot for the first tastes per year
    '''

    description = "first_taste_years \nDescription: There is a lot of variety in the first tastes of the chocolates rated 3.5 or higher. A consistent first taste over all years is 'creamy'. Other consistent tastes are 'complex', 'cherry' and 'fatty'. Otherwise the tastes are quite diverse. Feel free to look around with Plotly to get a more detailed view. "

    #select the examples with ratings 3.5 or higher
    highest_rating = df[df["rating"] >= 3.5]
    # group by the years and count the first tastes
    df2 = highest_rating.groupby("review date")["first taste"].value_counts().reset_index(name='counts')

    #create a scatter plot with different colors for different counts
    fig = px.scatter(df2, x = "review date", y = "first taste", color = "counts", width = 1000, height = 1800, title = "The first taste of all chocolates rated 3.5 or higher over the years")

    print(description)
    return fig

