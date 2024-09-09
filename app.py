# import the librareis 
import streamlit as st 
import pickle 
import numpy as np 
import pandas as pd 

st.set_page_config(layout="wide")

st.header("BOOK SAGE - A Book Recommendation System")

st.markdown('''
            #### Unveil a World of Tailored Reads, Crafted Just for You. 
            ''')

st.markdown('''
            ###### Explore. Discover. Read. Repeat. 
            ''')

# import our models : 

popular = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb')) 

# All Books

st.sidebar.title("All Books")

if st.sidebar.button("GET"):
    cols_per_row = 5 
    num_rows = 100 
    for row in range(num_rows): 
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row): 
            book_idx = row * cols_per_row + col
            if book_idx < len(books):
                with cols[col]:
                    st.image(books.iloc[book_idx]['Image-URL-M']) # Displays the image
                    st.text(books.iloc[book_idx]['Book-Title']) # Displays the Book Title
                    st.text(books.iloc[book_idx]['Book-Author']) # Display the Author name

# Top Books 

st.sidebar.title("Popular Books")

if st.sidebar.button("SHOW"):
    cols_per_row = 5 
    num_rows = 10 
    for row in range(num_rows): 
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row): 
            book_idx = row * cols_per_row + col
            if book_idx < len(popular):
                with cols[col]:
                    st.image(popular.iloc[book_idx]['Image-URL-M']) # Displays the image
                    st.text(popular.iloc[book_idx]['Book-Title']) # Displays the Book Title
                    st.text(popular.iloc[book_idx]['Book-Author']) # Display the Author name

# Function to Recommed Books 

def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x : x[1], reverse=True)[1:11]
    # Lets create empty list and in that lies i want to populate with the book information 
    # Book author book-title image url 
    # Empty list 
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item) 
    return data

# this is giving the names list of books. 
book_list = pt.index.values 

#Similar Books

st.sidebar.title("Similar Books")

# Drop down to select the books
selected_book = st.sidebar.selectbox("Select a book", book_list)

if st.sidebar.button("SUGGEST"):
    book_recommend = recommend(selected_book)
    num_cols = 5
    num_rows = 2
    for row in range(num_rows):
      cols = st.columns(num_cols)
      for col_idx in range(num_cols):
          book_idx = row * num_cols + col_idx
          if col_idx < len(book_recommend):
            with cols[col_idx]:
                  st.image(book_recommend[book_idx][2])
                  st.text(book_recommend[book_idx][0])
                  st.text(book_recommend[book_idx][1])


# import data
books = pd.read_csv('Data/Books.csv')  # Books data
users = pd.read_csv('Data/Users.csv') # Users data
ratings = pd.read_csv('Data/Ratings.csv') # Users Rating data

st.sidebar.title("Data Used")

if st.sidebar.button("EXPLORE"):
    st.subheader('Books Data used in the model')
    st.dataframe(books)
    st.subheader('User Ratings Data used in the model')
    st.dataframe(ratings)
    st.subheader('User Data used in the model')
    st.dataframe(users)













