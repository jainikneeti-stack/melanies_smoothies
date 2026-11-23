
# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

st.write(
    """Choose the fruits you want in your custom Smoothie"""
)

# Add name input box
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# Get the active Snowflake session
# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from the table
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME")
)

# Display the fruit options
# st.dataframe(data=my_dataframe, use_container_width=True)

# Convert Snowpark DataFrame into a list
fruit_options = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Allow users to select up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

# Create ingredients string
ingredients_string = ""

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

# Create SQL insert statement
my_insert_stmt = """
    INSERT INTO smoothies.public.orders
        (INGREDIENTS, NAME_ON_ORDER)
    VALUES (?, ?)
"""

# Submit Order button
time_to_insert = st.button("Submit Order")

if time_to_insert:
    if ingredients_list:

        # Insert smoothie order into Snowflake
        session.sql(
            my_insert_stmt,
            params=[
                ingredients_string.strip(),
                name_on_order
            ]
        ).collect()

        # Display success message
        st.success(
            f"Your Smoothie is ordered for {name_on_order}!",
            icon="✅"
        )

    else:
        st.warning("Please select at least one ingredient.")



