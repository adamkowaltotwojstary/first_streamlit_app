from urllib.error import URLError
import streamlit
import pandas
import requests
import snowflake.connector
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Brekfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected=streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index))
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
def get_fruityvice_data(fruit):
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit)
    return pandas.json_normalize(fruityvice_response.json())
    
    
streamlit.header('Fruityvice Fruit Advice')
try:
        fruit_choice=streamlit.text_input('What fruit would you like information about?')
        if not fruit_choice:
            streamlit.error('Please select a fruit to get information.')
        else:
            streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()


streamlit.header("View Our Fruit List- Add Your Favorites!")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_row)


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
        return "Thanks for adding "+ new_fruit
    
add_my_fruit=streamlit.text_input("What fruit would you like to add?")
if streamlit.button("Add a Fruit to the List"):
    my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_row_snowflake(add_my_fruit))      