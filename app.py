from flask import Flask, render_template, abort
import markdown2
import os
import chardet

app = Flask(__name__)

# Function to read and convert markdown files to HTML
def read_markdown_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
        content = file.read()
    return markdown2.markdown(content)

# Route to list all books
@app.route('/')
def index():
    summaries_dir = 'summaries'
    books = []
    
    for filename in os.listdir(summaries_dir):
        if filename.endswith('.md'):
            book_name = filename.replace('_', ' ').replace('.md', '')
            books.append(book_name)
    
    return render_template('index.html', books=books)

# Route to display a specific book summary
@app.route('/summary/<book_name>')
def summary(book_name):
    summaries_dir = 'summaries'
    file_path = os.path.join(summaries_dir, book_name.replace(' ', '_') + '.md')
    
    if not os.path.exists(file_path):
        abort(404)
    
    content = read_markdown_file(file_path)
    return render_template('summary.html', book_name=book_name, content=content)

if __name__ == '__main__':
    app.run(debug=True)
