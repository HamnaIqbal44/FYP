import streamlit as st
import altair as alt
import plotly.express as px

def category(df_processed, filtered_df):
    # label bar chart
    with st.container(border=True):
        # Count the occurrences of each predicted_label
        label_counts = df_processed['predicted_label'].value_counts().reset_index()
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
        sentiment_counts = filtered_df['predicted_label'].value_counts().reset_index()
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
