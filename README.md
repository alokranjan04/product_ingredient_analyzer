A Streamlit application that analyzes product ingredients from images using AI.
Features
📚 Example product analysis
📤 Upload product images
📸 Take photos of products
🔍 AI-powered ingredient analysis
📱 Mobile-responsive design
File Structure
text
product_ingredient_analyzer/
├── .streamlit/
│   └── config.toml
├── images/
│   ├── hide_and_seek.jpg
│   ├── bournvita.jpg
│   ├── lays.jpg
│   └── shampoo.jpg
├── app.py
├── constants.py
├── requirements.txt
└── README.md
Installation
Clone the repository:
bash
git clone https://github.com/alokranjan04/product_ingredient_analyzer.git
cd product_ingredient_analyzer
Install dependencies:
bash
pip install -r requirements.txt
Set up API keys in .streamlit/secrets.toml:
text
TAVILY_KEY = "your-tavily-api-key"
GEMINI_KEY = "your-gemini-api-key"
Usage
Run the Streamlit app:
bash
streamlit run app.py
Dependencies
streamlit
PIL
phi-agent
google-generativeai
tavily-python
Contributing
Fork the repository
Create your feature branch
Commit your changes
Push to the branch
Create a new Pull Request
License
This project is licensed under the MIT License.
GitHub Repository
Product Ingredient Analyzer