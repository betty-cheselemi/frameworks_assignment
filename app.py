import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from utils import load_and_clean_data

# Download and load data
@st.cache_data
def load_data():
    return load_and_clean_data()

def plot_publications_per_year(df, year_range):
    yearly = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]['year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    sns.barplot(x=yearly.index, y=yearly.values, ax=ax, palette='Blues')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Publications per Year')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_top_journals(df, year_range):
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    top_journals = filtered['journal'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax, palette='Greens')
    ax.set_xlabel('Number of Papers')
    ax.set_ylabel('Journal')
    ax.set_title('Top Journals')
    st.pyplot(fig)

def plot_wordcloud(df, year_range):
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    text = ' '.join(filtered['title'].dropna().astype(str))
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def plot_source_distribution(df, year_range):
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    source_counts = filtered['source_x'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(y=source_counts.index, x=source_counts.values, ax=ax, palette='Purples')
    ax.set_xlabel('Number of Papers')
    ax.set_ylabel('Source')
    ax.set_title('Distribution by Source')
    st.pyplot(fig)

def main():
    st.title('CORD-19 Metadata Analysis')
    st.markdown('''
    This app explores the CORD-19 dataset. Use the sidebar to filter by year and view:
    - Publications per year
    - Top journals
    - Wordcloud of title words
    - Distribution by source
    ''')
    
    # Load data with error handling
    try:
        df = load_data()
        if df is None:
            st.error("Failed to load data. Please check your Kaggle API credentials.")
            return
        
        min_year, max_year = int(df['year'].min()), int(df['year'].max())
        year_range = st.sidebar.slider('Select Year Range', min_year, max_year, (min_year, max_year))
        
        st.header('Publications per Year')
        plot_publications_per_year(df, year_range)
        
        st.header('Top Journals')
        plot_top_journals(df, year_range)
        
        st.header('Wordcloud of Title Words')
        plot_wordcloud(df, year_range)
        
        st.header('Distribution by Source')
        plot_source_distribution(df, year_range)
        
        st.header('Sample Data')
        filtered_data = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
        st.dataframe(filtered_data.head(20))
        
        # Show summary statistics
        st.header('Summary Statistics')
        st.write(f"Total papers in selected range: {len(filtered_data)}")
        st.write(f"Average abstract word count: {filtered_data['abstract_word_count'].mean():.1f}")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please ensure all dependencies are installed and Kaggle API is configured.")

if __name__ == '__main__':
    main()