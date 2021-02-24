from blog import app
import hashlib

@app.template_filter()
def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()
