from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    return "".join(page.extract_text() for page in pdf.pages)

def rank_resumes(job_desc, resumes):
    docs = [job_desc] + resumes
    tfidf = TfidfVectorizer().fit_transform(docs)
    return cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        job_desc = request.form.get('job_desc')
        files = request.files.getlist('resumes')
        
        if not job_desc or not files:
            return render_template('index.html', error="Please fill all fields")
        
        resumes = [extract_text_from_pdf(f) for f in files]
        scores = rank_resumes(job_desc, resumes)
        
        results = pd.DataFrame({
            'Resume': [f.filename for f in files],
            'Score': [round(score*100, 2) for score in scores]
        }).sort_values('Score', ascending=False)
        
        return render_template('index.html', results=results.to_html())
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)