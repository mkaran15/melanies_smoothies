# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


# option=st.selectbox("What is your favourite fruit?",
#             ("Banana","Strawberries", "Peaches")
#             )
# st.write("Your favourite fruit is: ",option)

# session=get_active_session()

cnx = st.connection("snowflake")
session=cnx.session()

name_on_order=st.text_input('Name on Smoothie: ')
st.write("The name on your smoothie will be: ",name_on_order)

my_dataframe=session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients: ",
    my_dataframe,
    max_selections=5
)
ingredients_string=''
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')
        st.subheader(each_fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        #st.text(smoothiefroot_response.json())
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        #st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#st.write(my_insert_stmt)

time_to_insert = st.button('Submit order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success("""Your Smoothie is ordered, """ + name_on_order + """!""", icon="✅")





