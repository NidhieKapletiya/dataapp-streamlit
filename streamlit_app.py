import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment")
st.subheader("~ by Nidhi Kapletiya")

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


#st.write("### (3) show a line chart of sales for the selected items in (2)")

if selected_sub_categories:
    # Further Filter Data Based on Sub-Categories
    filtered_data = filtered_by_category[filtered_by_category['Sub_Category'].isin(selected_sub_categories)]
    filtered_data = filtered_data.reset_index()  # Reset index for plotting

    # Aggregate Sales Data by Month
    sales_by_month = filtered_data.groupby(pd.Grouper(key="Order_Date", freq="M"))["Sales"].sum()

    # Line Chart for Selected Sub-Categories
    st.write("### Sales Over Time for Selected Sub-Categories")
    st.line_chart(sales_by_month, y="Sales")

    # Calculate Metrics
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # Calculate Overall Average Profit Margin
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    profit_margin_delta = profit_margin - overall_profit_margin

    # Display Metrics
    st.write("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%", f"{profit_margin_delta:.2f}%")
else:
    st.write("⚠️ Please select at least one Sub-Category to view data.")

