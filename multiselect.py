import streamlit as st
import plotly.express as px
import altair as alt
import pandas as pd
import os
import warnings
from streamlit_extras.metric_cards import style_metric_cards
from Feedback import suggestions
from scrap import process_dataframe_from_dashboard  # Importing the new function from scrap.py

warnings.filterwarnings('ignore')

# Page setting
st.set_page_config(page_title='Sentiment Analysis Dashboard', page_icon=':bar_chart:', layout='wide')
st.title(':bar_chart: Sentiment Analysis Dashboard')

# Add custom CSS for metrics section
st.markdown("""
    <style>
        div.block-container {
            padding-top:1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Uploading the CSV file
fl = st.file_uploader(":file_folder: Upload a file", type=["csv"])

if fl is not None:
    # Save the uploaded file temporarily
    temp_file_path = os.path.join(os.getcwd(), "temp_uploaded_file.csv")
    with open(temp_file_path, "wb") as f:
        f.write(fl.getbuffer())

    # Process the data using process_dataframe_from_dashboard function from scrap.py
    processed_df = process_dataframe_from_dashboard(temp_file_path)

    if processed_df is not None:
        st.success("File processed successfully with scrap.py")
        st.text("Processed DataFrame:")

        with st.sidebar:
            st.header("Sentiment Analysis DASHBOARD")
            selection = ['Review Dataset', 'Sentiment Analysis', 'Categorization', 'Suggestions']

            # Create radio buttons for dataset columns
            selected_column = st.radio(
                "Select the column to visualize",
                selection
            )
        if selected_column == 'Review Dataset':
            with st.expander("VIEW DATASET"):
                selected_columns = st.multiselect('Select the columns you want to view', options=processed_df.columns)

                # Check if any columns are selected
                if selected_columns:
                    # Display the dataframe with only the selected columns
                    st.dataframe(processed_df[selected_columns], use_container_width=True)
                else:
                    # Display a message when no columns are selected
                    st.write("Please select at least one column to view the data.")

        # Display metrics
        st.markdown('### Metrics')

        # Calculating metrics
        total_reviews = len(processed_df)
        positive_reviews = len(processed_df[processed_df['sentiment'] == 'POSITIVE'])
        negative_reviews = len(processed_df[processed_df['sentiment'] == 'NEGATIVE'])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews", total_reviews, delta="All Reviews")
        col2.metric("Positive Reviews", positive_reviews, delta="All Positive Reviews")
        col3.metric("Negative Reviews", negative_reviews, delta="All Negative Reviews")
        style_metric_cards(background_color="#00C49E", border_left_color='purple', border_color='purple')

        # Display the start and end date of the dataset
        col1, col2 = st.columns((2))
        processed_df["Date"] = pd.to_datetime(processed_df["Date"])
        startDate = processed_df["Date"].min()
        endDate = processed_df["Date"].max()

        with col1:
            date1 = pd.to_datetime(st.date_input("Start Date", startDate))
        with col2:
            date2 = pd.to_datetime(st.date_input("End Date", endDate))

        processed_df = processed_df[(processed_df["Date"] >= date1) & (processed_df["Date"] <= date2)].copy()
        processed_df['Date'] = pd.to_datetime(processed_df['Date'])

        df_filtered = processed_df[processed_df['sentiment'].isin(['POSITIVE', 'NEGATIVE'])]

        if selected_column == "Sentiment Analysis":
            # Bar Chart
            with st.container(border=True):
                # Count the occurrences of each predicted_label
                label_counts = processed_df['sentiment'].value_counts().reset_index()
                label_counts.columns = ['sentiment', 'count']

                # Create a bar chart using Altair
                chart = alt.Chart(label_counts).mark_bar().encode(
                    x=alt.X('sentiment:N', title='Sentiment'),
                    y=alt.Y('count:Q', title='Number of Reviews'),
                    color=alt.Color('sentiment:N', legend=alt.Legend(title="Sentiment")),
                    tooltip=['sentiment:N', 'count:Q']
                ).properties(
                    title='Sentiment Distribution',
                    width=650,  # Adjust the width of the figure
                    height=500  # Adjust the height of the figure
                ).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).configure_title(
                    fontSize=20
                )

                # Display the chart in Streamlit
                st.altair_chart(chart, use_container_width=True)

            # Donut chart
            with st.container(border=True):
                # Count the number of positive and negative sentiments
                sentiment_counts = df_filtered['sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['sentiment', 'count']

                # Create an interactive donut chart using Plotly
                fig = px.pie(sentiment_counts,
                             values='count',
                             names='sentiment',
                             title='Sentiment Distribution',
                             hole=0.5,  # To make it a donut chart
                             color='sentiment',
                             color_discrete_map={'POSITIVE': '#E6E6FA', 'NEGATIVE': '#AA336A'})

                # Update layout for dark theme and better aesthetics
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font=dict(color='white'),
                    title_font=dict(size=20),
                    # width=600,
                    # height=400
                )

                # Display the plot in the Streamlit app
                st.plotly_chart(fig, use_container_width=True)

        if selected_column == 'Categorization':
            # label bar chart
            with st.container(border=True):
                # Count the occurrences of each predicted_label
                label_counts = processed_df['predicted_label'].value_counts().reset_index()
                label_counts.columns = ['predicted_label', 'count']

                # Create a bar chart using Altair
                chart = alt.Chart(label_counts).mark_bar().encode(
                    x=alt.X('predicted_label:N', title='Predicted Label'),
                    y=alt.Y('count:Q', title='Number of Labels'),
                    color=alt.Color('predicted_label:N', legend=alt.Legend(title="Predicted Label")),
                    tooltip=['predicted_label:N', 'count:Q']
                ).properties(
                    title='Number of Labels per Predicted Label',
                    width=650,  # Adjust the width of the figure
                    height=500  # Adjust the height of the figure
                ).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).configure_title(
                    fontSize=20
                )

                # Display the chart in Streamlit
                st.altair_chart(chart, use_container_width=True)

            # label donut chart
            with st.container(border=True):
                # Count the number of positive and negative sentiments
                sentiment_counts = df_filtered['predicted_label'].value_counts().reset_index()
                sentiment_counts.columns = ['Label', 'count']

                # Create an interactive donut chart using Plotly
                fig = px.pie(sentiment_counts,
                             values='count',
                             names='Label',
                             title='Categorization',
                             hole=0.5,  # To make it a donut chart
                             color='Label')

                # Update layout for dark theme and better aesthetics
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font=dict(color='white'),
                    title_font=dict(size=20),
                    # width=600,
                    # height=400
                )

                # Display the plot in the Streamlit app
                st.plotly_chart(fig, use_container_width=True)

        if selected_column == 'Suggestions':
            suggestions(processed_df)

    else:
        st.error("Failed to process the file with scrap.py")
else:
    st.info("Please upload a file to proceed.")
