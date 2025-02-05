from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Sample FAQ data to train ai model
FAQS = [
    {
        "question": "What digital marketing services do you offer?",
        "answer": "We provide comprehensive digital marketing solutions including SEO, social media marketing, PPC advertising, content marketing, email marketing, web design, and analytics reporting."
    },
    {
        "question": "How long does it take to see results from SEO?",
        "answer": "SEO typically shows initial results in 3-6 months, depending on your website's current state, competition, and keyword strategy. Consistent efforts yield compounding growth over time."
    },
    {
        "question": "What's your pricing model?",
        "answer": "We offer flexible pricing including monthly retainers for ongoing services, project-based pricing for specific campaigns, and custom packages tailored to business needs."
    },
    {
        "question": "Do you have experience in our industry?",
        "answer": "Our team has worked with clients across various industries including e-commerce, healthcare, SaaS, and professional services. We customize strategies for each industry's unique needs."
    },
    {
        "question": "How do you measure campaign success?",
        "answer": "We track KPIs like website traffic, conversion rates, engagement metrics, ROI, and customer acquisition costs. You'll receive detailed monthly reports with performance insights."
    },
    {
        "question": "What's the minimum contract length?",
        "answer": "Our standard engagement is 6 months to allow proper strategy implementation and optimization. We do offer shorter trial periods for specific services."
    },
    {
        "question": "Do you handle social media management?",
        "answer": "Yes, our full-service social media management includes content creation, posting schedule, community management, paid advertising, and performance analytics."
    },
    {
        "question": "How often will we communicate?",
        "answer": "You'll have weekly check-ins with your account manager, monthly strategy reviews, and 24/7 access to our project management platform for ongoing communication."
    },
    {
        "question": "Can you work with our existing marketing team?",
        "answer": "Absolutely! We often collaborate with in-house teams to augment capabilities, provide specialized expertise, and handle overflow work."
    },
    {
        "question": "What platforms do you specialize in?",
        "answer": "We're certified experts in Google Ads, Microsoft Advertising, Facebook/Instagram Ads, LinkedIn Ads, Google Analytics, and all major SEO/SEM tools."
    }
]

client = Groq(api_key=os.environ.get("API KEY "))

def get_chat_response(user_input):
    try:
        # system prompt with FAQs
        system_prompt = f"""You are a helpful FAQ assistant. Base your answers on these FAQs:
        {chr(10).join([f"Q: {faq['question']} A: {faq['answer']}" for faq in FAQS])}
        If the question can't be answered with these FAQs, respond with 'I don't know'.
        If user says Hello then you just say Hello how can i help you today.
        if user asks you irrelevant questions like marry you or love you then just say sorry i am unable to help you.
        always give short and consise answers.do not make lengthy
        do not say hello in every question only say hello when user says hello to you
        """
        
        # Create the chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model="mixtral-8x7b-32768"
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = get_chat_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)