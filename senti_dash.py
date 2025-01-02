import streamlit as st
import altair as alt
import plotly.express as px
def sentiment(filtered_df):
    with st.container(border=True):
        # Count the occurrences of each predicted_label
        label_counts = filtered_df['sentiment'].value_counts().reset_index()
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
