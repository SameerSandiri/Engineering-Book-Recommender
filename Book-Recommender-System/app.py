from flask import Flask, render_template, request
import pickle
import difflib

# Load the data
books_data = pickle.load(open('books_data.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(books_data['Title'].values),
                           author=list(books_data['Authors'].values),
                           year=list(books_data['Year'].values),
                           language=list(books_data['Language'].values),
                           image=list(books_data['Image'].values),
                           branch=list(books_data['Branch'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    book_name = request.form.get('user_input')
    list_of_all_titles = books_data['Title'].tolist()

    # Find close matches for the provided book name
    find_close_match = difflib.get_close_matches(book_name, list_of_all_titles)

    # If no close matches found, return a message
    if not find_close_match:
        return "No close matches found for the book title."

    close_match = find_close_match[0]

    # Get the index of the closest matching book
    index_of_the_book = books_data[books_data.Title == close_match].index[0]

    # Calculate similarity scores
    similarity_score = list(enumerate(similarity[index_of_the_book]))

    # Sort the similar books based on similarity scores
    sorted_similar_books = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    print('Books suggested for you:\n')
    data = []

    # Loop through the sorted similar books and get the required information
    for i, item in enumerate(sorted_similar_books):
        if i >= 10:
            break

        index = item[0]

        # Retrieve Title, Authors, and Publisher based on the index
        book_info = books_data.loc[books_data.index == index, ['Title', 'Authors', 'Publisher', 'Branch']].values[0]
        title_from_index, authors_from_index, publisher_from_index, branch_from_index = book_info

        # Append the information to the data list
        data.append({'Title': title_from_index, 'Authors': authors_from_index, 'Publisher': publisher_from_index, 'Branch': branch_from_index})
    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
