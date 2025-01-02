import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

def expander(df_processed):
    with st.expander("VIEW DATASET"):
        selected_columns = st.multiselect('Select the columns you want to view', options=df_processed.columns)

        # Check if any columns are selected
        if selected_columns:
            # Display the dataframe with only the selected columns
            st.dataframe(df_processed[selected_columns], use_container_width=True)
        else:
            # Display a message when no columns are selected
            st.write("Please select at least one column to view the data.")

        # Display metrics
    st.markdown('### Metrics')

    # Calculating metrics
    total_reviews = len(df_processed)
    positive_reviews = len(df_processed[df_processed['sentiment'] == 'POSITIVE'])
    negative_reviews = len(df_processed[df_processed['sentiment'] == 'NEGATIVE'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reviews", total_reviews, delta="All Reviews")
    col2.metric("Positive Reviews", positive_reviews, delta="All Positive Reviews")
    col3.metric("Negative Reviews", negative_reviews, delta="All Negative Reviews")
    style_metric_cards(background_color="#00C49E", border_left_color='purple', border_color='purple')