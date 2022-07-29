import os
import ipywidgets as widgets
from IPython.display import display




class Best_fitting_chocolate:
    
    def __init__(self, df):
        '''
        Initializes all the widgets we need to represent the Chocolate finder
            Parameters: 
                df(dataframe): the preprocessed chocolate dataset
                
        '''
        
        #self.df_in: to have always the original dataset
        self.df_in = df
        #the filtered dataset
        self.df = df
       
       
        
        #Text for the usage of the chocolate finder
        first_message = widgets.HTML(
            value="<b>This is your personal chocolate finder, select all properties your chocolate should possess and get your favorite chocolate :)</b>",
            # placeholder='Some HTML',
            # description='Some HTML',
        )
        
       
        #the minimum and maximum of the cocoa percent in the dataset
        cocoa_min = min(self.df_in["cocoa percent"])
        cocoa_max = max(self.df_in["cocoa percent"])
        
        #Float Slider to select the cocoa percent of the chocolate
        self.cocoa_percent = widgets.FloatRangeSlider(
            value=[cocoa_min, cocoa_max],
            min=cocoa_min,
            max=cocoa_max,
            step=1,
            description='Cocoa percent:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )
        
        #search widget to find countries of bean origin
        self.search_widget = widgets.Text(description = 'search country')
        
        #widget to select all countries and deselect all countries
        self.all_widget = widgets.Checkbox(description='select all', value=False)
        self.none_widget = widgets.Checkbox(description='deselect all', value=False)
    
        #a set of all countries of bean origin in the dataset
        self.countries = sorted(set(self.df_in['country of bean origin']))
        #dictionary of checkbox widgets for all countries
        self.options_dict = {description: widgets.Checkbox(description=description, value=False) for description in self.countries}
        #all options in a list, which are used in the Vbox
        options = [self.search_widget] + [self.all_widget] + [self.none_widget] + [self.options_dict[description] for description in self.countries]
        self.bean_origin = widgets.VBox(options, layout={'overflow': 'scroll'})
        
        #search widget observes the search
        self.search_widget.observe(self.search, names='value')
        
        #interactive widget for interaction between the slider of cocoa percentage and bean origin
        interactive_percent_and_country = widgets.interactive(self.filter_cocoa_percent,  a=self.cocoa_percent)
        #interactive widget to select and deselect all countries
        interactive_select_deselect = widgets.interactive(self.select_deselect,  a=self.all_widget, b=self.none_widget)
              

            
        #making a Vbox consisting of one checkbox per ingredient
        self.ingredients = ('cocoa butter','vanilla','lecithin','salt','sugar','sweetener without sugar')
        self.ingredients_dict = {description: widgets.Checkbox(description=description, value=False) for description in self.ingredients}
        options_ingredients = [self.ingredients_dict[description] for description in self.ingredients]
        show_ingredients = widgets.VBox(options_ingredients, layout={'overflow': 'scroll'})
        
    
        
        #same as above, to select allergies
        self.allergies_dict = {description: widgets.Checkbox(description=description, value=False) for description in self.ingredients}
        options_allergies = [self.allergies_dict[description] for description in self.ingredients]
        show_allergies = widgets.VBox(options_allergies, layout={'overflow': 'scroll'})
        
        #list of interactive widgets to make sure that not the same ingredient and allergy can be ticked
        interactive_ingredients_allergies = [widgets.interactive(self.ingredients_allergies,i=widget1,a =widget2, d = description) for widget1,widget2,description in zip(options_ingredients,options_allergies,self.ingredients)]
        
        
        #making an accordion of all widgets and setting the titles
        accordion = widgets.Accordion(children=[self.cocoa_percent,self.bean_origin,show_ingredients, show_allergies])
        accordion.set_title(0,'Choose your cocoa percent!')
        accordion.set_title(1, 'From which countries should your cocoa beans be?')
        accordion.set_title(2, 'Which ingredients do you like?')
        accordion.set_title(3, 'Do you have any allergies or ingredients you do not want to have in your chocolate?')
        
        
        


        #shows at the end the found chocolates, at the beginning nothing
        self.end_message = widgets.HTML(value="")
        
        #for the first picture
        file = open("chocolade.picture.png", "rb")
        image = file.read()
        picture=widgets.Image(
            value=image,
            format='png',
            width=300,
            height=400,
        )
        
        #for the second picture
        file = open("chocolate.questionmark.jpg", "rb")
        image = file.read()
        picture2=widgets.Image(
            value=image,
            format='png',
            width=150,
            height=200,
        )
        
        
        
        #create a button to get the results, a button to get the next chocolate and a button to get back to the one before
        self.button = widgets.Button(description="Get your favourite chocolate(s)",
                                     layout=widgets.Layout(width='50%', height='50px'),
                                     button_style='success')
        
        self.button_next = widgets.Button(description="Next",
                                     layout=widgets.Layout(width='50%', height='50px'),
                                     button_style='info')
        self.button_back = widgets.Button(description="Back",
                                     layout=widgets.Layout(width='50%', height='50px'),
                                     button_style='info')
        #display the different widgets
        display(first_message)
        display(picture)
        display(accordion)
        
        display(self.button)
        #the button to show the results should observe if somebody pushed it
        self.button.on_click(self.on_button_clicked)

        display(self.end_message)
        #the next-button and back-button are hidden in the beginning
        self.button_next.layout.visibility = "hidden"
        self.button_back.layout.visibility = "hidden"
        display(self.button_back)
        display(self.button_next)
        
        display(picture2)
        

      
    def select_deselect(self,a,b):
        
        '''
        Function to set all Checkbox values of the countries of bean origin to True,
        if 'select all' was activated or False if 'deselect all' was activated
            Parameters: 
                a(boolean): value of the Checkbox 'select all'
                b(boolean): value of the Checkbox 'deselect all'
        '''
        
        for description in sorted(set(self.df_in['country of bean origin'])):
            if a:
                self.options_dict[description].value = True
                #set all Checkboxes to disabled as long as the Checkbox 'select all' is aktivated
                self.options_dict[description].disabled = True
                self.none_widget.disabled = True
            elif b: 
                self.options_dict[description].value = False
                self.options_dict[description].disabled = True
                self.all_widget.disabled = True
                
            else: 
                #if both are not activated, set disabled of False
                self.options_dict[description].disabled = False
                self.all_widget.disabled = False
                self.none_widget.disabled = False


    def filter_cocoa_percent(self,a):
        
        '''
        Function to filter the dataset if the cocoa percent slider was used and update the list of countries accordingly
        (to get an a bit smaller selection of countries of bean origin)
            Parameters: 
                a(tuple): the value of the slider 'self.cocoa_percent'
                
        '''
        
        #filter the dataset
        cocoa_min = a[0]
        cocoa_max = a[1]
        self.df = self.df_in[self.df_in['cocoa percent'] >= cocoa_min]
        self.df = self.df[self.df['cocoa percent'] <= cocoa_max]
        
        #get new selection of countries
        self.countries = sorted(set(self.df['country of bean origin']))
        #call search to make sure that the text in the search field won't get lost (search will then update the VBox)
        self.search({'new':self.search_widget.value})
         

    def search(self,change):
        
        '''
        Function to search for countries
            Parameters: 
                change(dictionary): dictionary with the changes of 'self.search_widget'

        '''
        search_input = change['new']
     
        #if search_input is empty: reset the list of countries
        if search_input == '':
            matches = self.countries
            

        else:
            #matches are all countries, which are beginning with the search_input
            matches = [description for description in self.countries if description.startswith(search_input)]
        
        #update the list of options with just the Checkboxes of matching countries    
        new_options = [self.search_widget] + [self.all_widget]  + [self.none_widget] + [self.options_dict[description] for description in matches]
        #set the children of self.bean_origin to new_options
        self.bean_origin.children = new_options
                
        
    def ingredients_allergies(self, i,a,d):
        '''
        Function to set, when ticked the Checkbox auf an ingredient, the corresponding Checkbox of allergies disabled
        and vice versa
            Parameters: 
                i(boolean): value of the ingredient
                a(boolean): value of the allergy
                d(str): description (key for the dictonary)
        '''
        if i:
            self.allergies_dict[d].disabled = True
        elif a:
            self.ingredients_dict[d].disabled = True
        else: 
            self.allergies_dict[d].disabled = False
            self.ingredients_dict[d].disabled = False

        
    def on_button_clicked(self,b):
        '''
        Function, which is called if the button for the results is pushed.
        It filters the dataset and if it isn't empty, it calles a function to print out the different chocolates. 
                b(boolean): value of 'self.button'
        '''
        
        #filters the cocoa percent 
        cocoa_min = self.cocoa_percent.value[0]
        cocoa_max = self.cocoa_percent.value[1]

        self.df = self.df_in[self.df_in['cocoa percent'] >= cocoa_min]
        self.df = self.df[self.df['cocoa percent'] <= cocoa_max]
        
        #filters the dataset according to the values of countries of bean origin
        if not(self.df.empty):
            if not(self.all_widget.value):
                for description in self.countries:
                    if not(self.options_dict[description].value):
                        self.df = self.df[self.df['country of bean origin'] != description]
                        
                       
                        
        #filters the dataset according to the wished ingredients and allergies
        for description in self.ingredients:
            if not(self.df.empty):
                if self.ingredients_dict[description].value:
                    self.df = self.df[self.df[description] == 'have ' + description]
                if self.allergies_dict[description].value:
                    self.df = self.df[self.df[description] == 'have not ' + description]

        #if the dataset is empty, set end message value and let the button observe if it is pushed again              
        if self.df.empty:
            self.end_message.value = "Your favorite chocolate unfortunately doesn't exist, try to be a bit more general!"
            self.button_next.layout.visibility = "hidden"
            self.button_back.layout.visibility = "hidden"
            self.button.on_click(self.on_button_clicked)
        
        #else: set 'zaehler' to 0, get the number of chocolates, reset index of the dataframe and call on_button_next_clicked        
        else:
            self.zaehler = 0
            self.anzahl = len(self.df)
            self.df.index = range(0,self.anzahl)
            self.button_back.layout.visibility = "hidden"
            self.on_button_next_clicked(True)
            
    def on_button_next_clicked(self,b):
        '''
        Function for setting the 'end_message' to the filtered chocolates and to control the visibility of
        'button_back' and 'button_next'
         
                b(boolean): value of 'button_back'
        '''
        #if we don't show the first chocolate at the moment, the back-button is visible and should observe if it is pushed
        if self.zaehler > 0:
            self.button_back.layout.visibility = "visible"
            self.button_back.on_click(self.on_button_back_clicked) 
        
        #getting all information, we need for representing the chocolates and updating the end_message
        ingredients = "beans"
        for i in self.ingredients:
            if self.df[i][self.zaehler] == "have " + i:
                ingredients = ingredients + ", " + i


        tastes = self.df['first taste'][self.zaehler] + ", " + self.df['second taste'][self.zaehler] + ", " + self.df['third taste'][self.zaehler]
        tastes = tastes.replace(", no information", "")

        self.end_message.value = "<br><b>Your best chocolate(s):</b><br><br><b>Rating:</b>  " + str(self.df['rating'][self.zaehler]) + "<br><b>Country of bean origin:</b>  " + self.df['country of bean origin'][self.zaehler] + "<br><b>Cocoa percent:</b>  " + str(self.df['cocoa percent'][self.zaehler]) + "<br><b>Taste:</b>  " + tastes + "<br><b>Ingredients:</b>  " + ingredients + "<br><b>Company:</b>  " + self.df['company'][self.zaehler] + "<br><b>Company Location:</b>  " + self.df['company location'][self.zaehler] + "<br><br>Chocolate " + str(self.zaehler + 1) + "/" + str(self.anzahl) 
        
        #if the 'zaehler' is still smaller than 'anzahl', increase it 
        if self.anzahl > self.zaehler:
            self.zaehler = self.zaehler + 1
            
        #if we are not showing our last chocolate at the moment, the next-button should be visible and observe if it is pushed
        if self.anzahl > self.zaehler:
            self.button_next.layout.visibility = "visible"            
            self.button_next.on_click(self.on_button_next_clicked)
        else: 
            self.button_next.layout.visibility = "hidden"
        
        #let the button for the filtering observe if it is pushed again
        self.button.on_click(self.on_button_clicked)  
          
    
    def on_button_back_clicked(self,b):
        '''
        Function, which is called if the back-button is pushed.
        It resets the 'zaehler', checks if the back-button still should be visible and calls 'on_button_next_clicked' again
                b(boolean): value of 'self.button_back'
        '''
        if self.zaehler > 0:
            self.zaehler = self.zaehler - 2
            
        if self.zaehler <= 0:
            self.button_back.layout.visibility = "hidden"
            self.zaehler = 0
            
        self.on_button_next_clicked(True)
       



        
        
  