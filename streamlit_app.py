import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

#st.write("## Your additions")
#st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

# Dropdown menu for category selection
category_options = df['Category'].unique()  # Extract unique categories from the DataFrame
selected_category = st.selectbox("Select a Category", category_options)

# Filter the DataFrame based on selected category
filtered_by_category = df[df['Category'] == selected_category]

# Display the filtered data
#st.write(f"### Filtered Data for Category: {selected_category}")
#st.dataframe(filtered_by_category)

#st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")

# Multi-select for Sub_Category within selected Category
sub_category_options = filtered_by_category['Sub_Category'].unique()  # Get unique sub-categories
selected_sub_categories = st.multiselect("Select Sub-Categories", sub_category_options)

# Filter data further based on selected Sub_Categories
filtered_data = filtered_by_category[filtered_by_category['Sub_Category'].isin(selected_sub_categories)]

# Display the filtered data
st.write(f"### Filtered Data for Category: {selected_category} and Sub-Categories: {', '.join(selected_sub_categories) if selected_sub_categories else 'None'}")
st.dataframe(filtered_data)

st.write("### (3) show a line chart of sales for the selected items in (2)")


filtered_data = filtered_data.reset_index()  # 'Order_Date' will now be a column again

st.write(filtered_data.columns)
filtered_data['Month'] = filtered_data['Order_Date'].dt.month_name()

# Line chart for selected subcategory
if not filtered_data.empty:
    st.write("Sales Trend")
    sales_trend_data = filtered_data.groupby('Month')['Sales'].sum().reset_index()  # Aggregate sales by month
    sales_trend_data = sales_trend_data.set_index('Month')  # Set month as index for the line chart
    st.line_chart(sales_trend_data)
else:
    st.write("No data available for the selected filters.")

# Add numerical month to help with sorting
filtered_data['Month_Number'] = filtered_data['Order_Date'].dt.month
filtered_data['Month'] = filtered_data['Order_Date'].dt.month_name()

# Group by Sub_Category, Month_Number, and Month to preserve the order and sub-category breakdown
sales_trend_data = filtered_data.groupby(['Sub_Category', 'Month_Number', 'Month'])['Sales'].sum().reset_index()

# Sort the data by Month_Number to ensure correct order
sales_trend_data = sales_trend_data.sort_values('Month_Number')

# Pivot the table so that each Sub_Category has its own column
sales_trend_pivot = sales_trend_data.pivot(index='Month', columns='Sub_Category', values='Sales')

# Plot the line chart
st.line_chart(sales_trend_pivot)

# Add numerical month to help with sorting
filtered_data['Month_Number'] = filtered_data['Order_Date'].dt.month
filtered_data['Month'] = filtered_data['Order_Date'].dt.month_name()

# Group by Sub_Category, Month_Number, and Month to preserve the order and sub-category breakdown
sales_trend_data = filtered_data.groupby(['Sub_Category', 'Month_Number', 'Month'])['Sales'].sum().reset_index()

# Sort the data by Month_Number to ensure correct chronological order
sales_trend_data = sales_trend_data.sort_values('Month_Number')

# Pivot the table so that each Sub_Category has its own column
sales_trend_pivot = sales_trend_data.pivot(index='Month_Number', columns='Sub_Category', values='Sales')

# Replace the Month_Number index with actual month names (in the correct order)
sales_trend_pivot.index = sales_trend_data.drop_duplicates('Month_Number').set_index('Month_Number')['Month']

# Plot the line chart with the months in the correct order
st.line_chart(sales_trend_pivot)

import calendar

# Add numerical month to help with sorting
filtered_data['Month_Number'] = filtered_data['Order_Date'].dt.month
filtered_data['Month'] = filtered_data['Order_Date'].dt.month_name()

# Group by Sub_Category, Month_Number, and Month to preserve the order and sub-category breakdown
sales_trend_data = filtered_data.groupby(['Sub_Category', 'Month_Number', 'Month'])['Sales'].sum().reset_index()

# Explicitly define the order of months using pandas Categorical
sales_trend_data['Month'] = pd.Categorical(sales_trend_data['Month'], categories=list(calendar.month_name[1:]), ordered=True)

# Sort the data by the Month categorical order
sales_trend_data = sales_trend_data.sort_values('Month')

# Pivot the table so that each Sub_Category has its own column
sales_trend_pivot = sales_trend_data.pivot(index='Month', columns='Sub_Category', values='Sales')

# Plot the line chart with the months in the correct order
st.line_chart(sales_trend_pivot)

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
