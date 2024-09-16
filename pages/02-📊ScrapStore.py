import streamlit as st
from code_utils.auth import login_st_form
import requests
import pandas as pd
import json
import plotly.express as px
from streamlit_lottie import st_lottie
from re import findall
from bs4 import BeautifulSoup
from df_global_search import DataFrameSearch
import nltk
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

st.set_page_config(page_title='ScrapStore', page_icon=':bar_chart:', initial_sidebar_state="auto", menu_items=None)

st.title(':bar_chart: ScrapStore')
st.subheader('Spy all your Ecommerce competitors to replicate their success :dollar:')

logged_in = login_st_form()


class ShopifyScraper():

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def downlaodjson(self, page):
        r = requests.get(self.baseurl + f'/products.json?limit=250&page={page}', timeout=5)
        if r.status_code != 200:
            st.warning('Bad Status : ', r.status_code)
        if len(r.json()['products']) > 0:
            data = r.json()['products']
            return data
        else : 
            return 
    
    def parsejson(self, jsondata):
        products = []
        for prod in jsondata:
            mainid = prod['id']
            title = prod['title']
            published_at = prod['published_at']
            product_type = prod['product_type']
            for variant in prod['variants']:
                item = {
                    'id': mainid,
                    'title' : title,
                    'published_at': published_at,
                    'product_type' : product_type,
                    'varid' : variant['id'],
                    'vartitle' : variant['title'],
                    'sku' : variant['sku'],
                    'price': variant['price'],
                    'available' : variant['available'],
                    'created_at' : variant['created_at'],
                    'updated_at' : variant['updated_at'],
                    'compare_at_price' : variant['compare_at_price']
                }
                products.append(item)
            #return st.dataframe(products)
        
    def display_graph(self, page):
        products = []
        r = requests.get(self.baseurl + f'/products.json?limit=250&page={page}', timeout=5)
        if r.status_code != 200:
            st.warning('Bad Status : ', r.status_code)
        if len(r.json()['products']) > 0:
            data = r.json()['products']
            for prod in data:
                mainid = prod['id']
                title = prod['title']
                published_at = prod['published_at']
                product_type = prod['product_type']
                for variant in prod['variants']:
                    item = {
                        'id': mainid,
                        'title' : title,
                        'published_at': published_at,
                        'product_type' : product_type,
                        'varid' : variant['id'],
                        'vartitle' : variant['title'],
                        'sku' : variant['sku'],
                        'price': variant['price'],
                        'available' : variant['available'],
                        'created_at' : variant['created_at'],
                        'updated_at' : variant['updated_at'],
                        'compare_at_price' : variant['compare_at_price']
                    }
                    products.append(item)
            df = st.dataframe(products)
            product_type = [c['product_type'] for c in products]
            title_product = [c['title'] for c in products]
            price = [c['price'] for c in products]
            #convert to pandas dataframe
            df_pandas = pd.DataFrame({'product_type':product_type, 'title':title_product, 'price':price})
            st.dataframe(df_pandas)
            st.sidebar.subheader("Please Filter Here")
            prod_type = st.sidebar.multiselect(
                "Select the product type:",
                options=df_pandas["product_type"].unique(),
                default=df_pandas["product_type"].unique()
            )
            title_prod = st.sidebar.multiselect(
                "Select Title product:",
                options=df_pandas["title"].unique(),
                default=df_pandas["title"].unique()
            )
            df_selection = df_pandas.query(
                "product_type==@prod_type & title== @title_prod "
            )

            #KPI's
            total_product_sale = len(df_selection["product_type"])
            total_title = len(df_selection["title"])
            #display KPI's
            left_column, middle_column = st.columns(2)
            with left_column:
                st.subheader("Total products sales:")
                st.subheader(f"{total_product_sale} :shopping_bags:")
            with middle_column:
                st.subheader("Total Titles products:")
                st.subheader(f"{total_title} :bookmark:")
                #return st.dataframe(products)
                #display charts
            quantity_product_type = (
                df_selection.groupby(by=['product_type']).sum().head(8)
            )
            fig_product_sales = px.bar(
            quantity_product_type,
            x=df_selection["price"].head(8),
            y=quantity_product_type.index,
            orientation="h",
            title="<b>Price by Product Type on the store</b>",
            color_discrete_sequence=["#205295"] * len(quantity_product_type),
            template="plotly_white",
            )

            fig_product_sales.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False))
            )
            #displaying chart
            st.plotly_chart(fig_product_sales,use_container_width=True)
#function permit to upload csv file a display charts
    #create function to display the lottie
def display_dataframe_shopifyer():
    url = "https://xpareto.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        #find all the title of the dataframe
        title = []
        for element in soup.find_all('a', {'class' : 'sortSize'}):
            #print(element.text)
            title.append(element)
        #store_adress = []
        #store_adress = [adress.get('href') for adress in soup.find_all('a', {'target' : '_blank'})]
        example = []
        example = [adress.find_parent().find('a').text for adress in soup.find_all('a', {'target': '_blank'})]
        list_example = set(example)
        while 'Click Here' in example : 
            del example[example.index('Click Here')]
        #print(store_adress)
        #print(example)
        #print('###########')
        #print('#############')
        #crÃ©er une liste de sous liste pour stocker les donnÃ©es
        daily_trafic = []
        daily_trafic = [trafic.text for trafic in soup.find_all('div', {'class' : 'col-xs-2 tborder'})]
        for element in daily_trafic: 
            while 'Click Here' in daily_trafic:
                del daily_trafic[daily_trafic.index('Click Here')]
            for e in element: 
                while 'Best Selling' in daily_trafic:
                    del daily_trafic[daily_trafic.index('Best Selling')]
                for el in e : 
                    while 'Daily Traffic' in daily_trafic:
                        del daily_trafic[daily_trafic.index('Daily Traffic')]
        

        #print(daily_trafic)

        #retrieve rating data
        rating_data = []
        rating_data = [element.text for element in soup.find_all('div', {'class' : 'col-xs-1 tborder'})]
        for element in rating_data: 
            while 'Rating' in rating_data:
                del rating_data[rating_data.index('Rating')]
        #print('#############')
        #print(rating_data)
        #print("############")

        #retrieve the best seller product url
        best_sellings_products = []
        child_div = soup.find_all('a', {'target' : '_blank'})
        child_parent = soup.find_all('div', {'class': 'col-xs-2 tborder'})
        #child_div = [element.get('href') for element in child_div if soup.find('div', {'class' : 'col-xs-2'})]
        child_div = [child.find_parent('div', {'class': 'col-xs-2 tborder'}) for child in child_div]
        for element in soup.find_all('a'):
            href = element.attrs['href']
            if href.endswith("best-selling"):
                best_sellings_products.append(str(element.attrs['href']))
        #contains all the urls include the best product sellings
        #print(best_sellings_products)

        #put all the data in a dataframe
        #create a dict to transform in a dataframe
        data_dict = {'Store Adress':example, 'Daily Trafic': daily_trafic, 'Best Selling':best_sellings_products}
        #convert to a dict 
        #print('##############')
        #print(len(example))
        #print(len(daily_trafic))
        #print(len(rating_data))
        #suppression de 99 data dans cette liste
        del rating_data[100:199]
        print(len(rating_data))
        print(len(best_sellings_products))
        df = pd.DataFrame(data_dict)
        st.dataframe(df)
        #print(df)
        #create a database to store the data and managing data using the playground
                    
                
                
                #print(str(element.attrs['href'])+"\n")
                    
        
        #parent_div = [child.find_parent('div', {'class' : 'col-xs-2 tborder'}) for child in child_div]
        #best_sellings_products.append(parent_div)
        #print(best_sellings_products)
        #print(child_div)
#function to insert the lottie
def lottiefile(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

def display_sheets():
    df = pd.read_csv("Shopify_stores_list.xlsx")
    st.write(df)

#function SEO analyzer
def seo_analysis(url):
# Save the good and the warnings in lists
    good = []
    bad = []
# Send a GET request to the website
    response = requests.get(url)
# Check the response status code
    if response.status_code != 200:
        print("Error: Unable to access the website.")
        return

# Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

# Extract the title and description
    title = soup.find('title').get_text()
    description = soup.find('meta', attrs={'name': 'description'})['content']

# Check if the title and description exist
    if title:
        good.append("Title Exists! Great!")
    else:
        bad.append("Title does not exist! Add a Title")

    if description:
        good.append("Description Exists! Great!")
    else:
        bad.append("Description does not exist! Add a Meta Description")

# Grab the Headings
    hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    h_tags = []
    for h in soup.find_all(hs):
        good.append(f"{h.name}-->{h.text.strip()}")
        h_tags.append(h.name)

    if 'h1' not in h_tags:
        bad.append("No H1 found!")

# Extract the images without Alt
    for i in soup.find_all('img', alt=''):
        bad.append(f"No Alt: {i}") 

# Extract keywords
# Grab the text from the body of html
    bod = soup.find('body').text

# Extract all the words in the body and lowercase them in a list
    words = [i.lower() for i in word_tokenize(bod)]

# Grab a list of English stopwords
    sw = nltk.corpus.stopwords.words('english')
    new_words = []

# Put the tokens which are not stopwords and are actual words (no punctuation) in a new list
    for i in words:
      if i not in sw and i.isalpha():
        new_words.append(i)

# Extract the fequency of the words and get the 10 most common ones
    freq = nltk.FreqDist(new_words)
    keywords= freq.most_common(10)

# Print the results
    st.write("Keywords: ", keywords)
    #st.write("The Good: ", good)
    #st.write("The Bad: ", bad)
    
# Call the function to see the results
#seo_analysis("https://pythonology.eu/what-is-syntax-in-programming-and-linguistics/")


 
            
def main():
    st.markdown('Presentation in synthetic forms of data from numerous e-commerce stores with some success and constantly updated according to monthly results.')
    st.markdown('**ScrapStore** updates its data automatically in order to inform you as much as possible of new scraper e-commerce stores...')
    #display_dataframe_shopifyer()
    #code du lottie
    search_bar_columns = st.columns((2, 1, 0.5, 0.75, 1))
    with search_bar_columns[4]:
        highlight_match = st.toggle("Highlight Matching Cells", value=True)
    #display_sheets()


#st_lottie(lottie_logo, key="Logo")

    with st.form(key='Shopify_scraper_form'):
        base_domain = st.text_input('Enter your domain', placeholder='https://www.store.com')
        submit_button = st.form_submit_button(label='Search')
        number_button = st.number_input("Insert a number", value=1)
        #limit = st.slider('How many tweets do you want to get?', 0, 500, step=20)
        #output_csv = st.radio('Save a CSV file?', ['Yes', 'No'])
        #file_name = st.text_input('Name the Database:', placeholder='Enter the database name')
        if submit_button:
            #display_dataframe_shopifyer()
            store_data = ShopifyScraper(base_domain)
            data = store_data.downlaodjson(int(number_button))
            store_data.parsejson(data)
            store_data.display_graph(base_domain)
    #st.title(':male-detective: Keywords And SEO Anlayzer')
    #st.markdown('The main keywords present on the store and with which the SEO strategy is carried out')
    #with st.form(key='SEO analyszer'):
        #text_input = st.text_input('Enter the url', placeholder='https://www.store.com')
        #seo_button = st.form_submit_button(label='Search')
        #if seo_button:
            #seo_analysis(text_input)

if logged_in:
    st.success('You are logged in!')
    st.balloons()
    #st.markdown('Add Your Streamlit App Here!')
    main()

hide_st_style="""
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)

    
