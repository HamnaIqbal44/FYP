import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from streamlit_extras.metric_cards import style_metric_cards
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
        st.write(processed_df)

        # Calculating metrics
        total_reviews = len(processed_df)
        positive_reviews = len(processed_df[processed_df['sentiment'] == 'POSITIVE'])
        negative_reviews = len(processed_df[processed_df['sentiment'] == 'NEGATIVE'])

        # Display metrics
        st.markdown('### Metrics')
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews", total_reviews, delta="All Reviews")
        col2.metric("Positive Reviews", positive_reviews, delta="All Positive Reviews")
        col3.metric("Negative Reviews", negative_reviews, delta="All Negative Reviews")
        style_metric_cards(background_color="#262730", border_left_color='#00C49E')

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

        # bar chart
        # Count the number of reviews for each date
        # selecting 2 bar chart columns
        # Create columns for side-by-side charts
        col1, col2 = st.columns(2)

        # Filter out only positive and negative sentiments
        df_filtered = processed_df[processed_df['sentiment'].isin(['POSITIVE', 'NEGATIVE'])]

        # First plot: Sentiment distribution
        with col1:
            sentiment_counts = df_filtered['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']

            fig1 = px.bar(sentiment_counts,
                          x='sentiment',
                          y='count',
                          color='sentiment',
                          title='Sentiment Distribution',
                          labels={'sentiment': 'Sentiment', 'count': 'Number of Reviews'},
                          color_discrete_map={'POSITIVE': '#C3B1E1', 'NEGATIVE': '#DA70D6'})

            fig1.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='white'),
                title_font=dict(size=20),
                xaxis=dict(title='Sentiment', tickmode='array', tickvals=['POSITIVE', 'NEGATIVE']),
                yaxis=dict(title='Number of Reviews'),
                width=600,  # Adjust the width of the figure
                height=500  # Adjust the height of the figure
            )

            st.plotly_chart(fig1)

        # Second plot: Sentiment distribution per date
        with col2:
            df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])
            sentiment_date_counts = df_filtered.groupby(['Date', 'sentiment']).size().reset_index(name='count')

            fig2 = px.bar(sentiment_date_counts,
                          x='Date',
                          y='count',
                          color='sentiment',
                          barmode='group',
                          title='Sentiment Distribution per Date',
                          labels={'Date': 'Date', 'count': 'Number of Reviews'},
                          color_discrete_map={'POSITIVE': '#00C49E', 'NEGATIVE': 'purple'})

            fig2.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='white'),
                title_font=dict(size=20),
                width=650,  # Adjust the width of the figure
                height=500  # Adjust the height of the figure
            )

            st.plotly_chart(fig2)

        col1, col2 = st.columns(2)

        with col1:
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
                width=600,
                height=400
            )

            # Display the plot in the Streamlit app
            st.plotly_chart(fig)

        with col2:
            # Filter out only positive and negative sentiments
            df_filtered = processed_df[processed_df['sentiment'].isin(['POSITIVE', 'NEGATIVE'])]

            # Convert the date column to datetime format
            df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])

            # Count the number of positive and negative sentiments per date
            sentiment_date_counts = df_filtered.groupby(['Date', 'sentiment']).size().reset_index(name='count')

            # Create an interactive line graph using Plotly
            fig = px.line(sentiment_date_counts,
                          x='Date',
                          y='count',
                          color='sentiment',
                          title='Sentiment Trend Over Time',
                          labels={'Date': 'Date', 'count': 'Number of Reviews'},
                          color_discrete_map={'POSITIVE': '#00C49E', 'NEGATIVE': 'purple'})

            # Update layout for dark theme and better aesthetics
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='white'),
                title_font=dict(size=20),
                xaxis=dict(title='Date', tickmode='auto'),
                yaxis=dict(title='Number of Reviews'),
            )

            # Display the plot in the Streamlit app
            st.plotly_chart(fig)

    else:
        st.error("Failed to process the file with scrap.py")

else:
    st.info("Please upload a file to proceed.")
