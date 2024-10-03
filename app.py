from flask import Flask, request, render_template

app = Flask(__name__)

# Fungsi untuk memformat teks
def prepare_text(text):
    text = text.upper().replace(' ', '').replace('J', 'I')
    prepared_text = ''
    
    i = 0
    while i < len(text):
        first = text[i]
        second = text[i + 1] if (i + 1) < len(text) else 'X'
        
        if first == second:
            second = 'X'
        else:
            i += 1
        
        prepared_text += first + second
        i += 1
    
    if len(prepared_text) % 2 != 0:
        prepared_text += 'X'
    
    return prepared_text

# Fungsi untuk membangun matriks Playfair
def build_matrix(keyword):
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    matrix = []
    used_chars = []
    
    keyword = keyword.upper().replace('J', 'I')
    
    for char in keyword:
        if char not in used_chars:
            matrix.append(char)
            used_chars.append(char)
    
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.append(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]

# Fungsi untuk mencari posisi karakter di dalam matriks
def get_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

# Fungsi enkripsi Playfair
def encrypt(text, matrix):
    text = prepare_text(text)
    cipher_text = ''
    
    for i in range(0, len(text), 2):
        first_char = text[i]
        second_char = text[i + 1]
        
        row1, col1 = get_position(matrix, first_char)
        row2, col2 = get_position(matrix, second_char)
        
        if row1 == row2:
            cipher_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    
    return cipher_text

# Fungsi dekripsi Playfair
def decrypt(cipher_text, matrix):
    plain_text = ''
    
    for i in range(0, len(cipher_text), 2):
        first_char = cipher_text[i]
        second_char = cipher_text[i + 1]
        
        row1, col1 = get_position(matrix, first_char)
        row2, col2 = get_position(matrix, second_char)
        
        if row1 == row2:
            plain_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plain_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            plain_text += matrix[row1][col2] + matrix[row2][col1]
    
    return plain_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        keyword = request.form['keyword']
        operation = request.form['operation']
        
        matrix = build_matrix(keyword)
        if operation == 'encrypt':
            result = encrypt(text, matrix)
        else:
            result = decrypt(text, matrix)
    else:
        result = ''
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
