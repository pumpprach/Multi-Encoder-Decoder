from flask import Flask, request, render_template
import base64
import binascii
import hashlib

app = Flask(__name__)

def to_base64(text):
    return base64.b64encode(text.encode()).decode()

def from_base64(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return None

def to_base32(text):
    return base64.b32encode(text.encode()).decode()

def from_base32(text):
    try:
        return base64.b32decode(text.encode()).decode()
    except Exception:
        return None

def to_hex(text):
    return text.encode().hex()

def from_hex(text):
    try:
        return bytes.fromhex(text).decode()
    except Exception:
        return None

def to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def from_binary(text):
    try:
        return ''.join(chr(int(b, 2)) for b in text.split())
    except Exception:
        return None

def to_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    
    if request.method == 'POST':
        text = request.form.get('text')
        method = request.form.get('method')

        # Validate based on selected method
        if method == 'from_base64' and not is_base64(text):
            error = "Invalid Base64 input. Please use the correct format."
        elif method == 'from_base32' and not is_base32(text):
            error = "Invalid Base32 input. Please use the correct format."
        elif method == 'from_hex' and not is_hex(text):
            error = "Invalid Hex input. Please use the correct format."
        elif method == 'from_binary' and not is_binary(text):
            error = "Invalid Binary input. Please use the correct format."
        else:
            # Call the appropriate function
            if method == 'to_base64':
                result = to_base64(text)
            elif method == 'from_base64':
                result = from_base64(text)
            elif method == 'to_base32':
                result = to_base32(text)
            elif method == 'from_base32':
                result = from_base32(text)
            elif method == 'to_hex':
                result = to_hex(text)
            elif method == 'from_hex':
                result = from_hex(text)
            elif method == 'to_binary':
                result = to_binary(text)
            elif method == 'from_binary':
                result = from_binary(text)
            elif method == 'to_md5':
                result = to_md5(text)

    return render_template('index.html', result=result, error=error)

def is_base64(s):
    try:
        if isinstance(s, str):
            # Check if string is valid Base64
            return base64.b64encode(base64.b64decode(s.encode())).decode() == s
        return False
    except Exception:
        return False

def is_base32(s):
    try:
        if isinstance(s, str):
            # Check if string is valid Base32
            return base64.b32encode(base64.b32decode(s.encode())).decode() == s
        return False
    except Exception:
        return False

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def is_binary(s):
    return all(bit in '01 ' for bit in s)

if __name__ == '__main__':
    app.run(debug=True)
