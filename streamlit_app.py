# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# adding streamlit connect as per lesson 8 to move from SiS to SniS
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """    Choose the fruits you want in your custom smoothie!
    """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# commenting out session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('Fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose Up To 5 Ingredients:'
    , my_dataframe
    , max_selections=5
    )

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

#    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

#    if ingredients_string:
#        session.sql(my_insert_stmt).collect()
#       st.write(name_on_order)
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
#        st.success('Your Smoothie is ordered!', icon="✅")

# Adding smoothiefruit api call support - new section to display smoothiefroot nutrituion information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
