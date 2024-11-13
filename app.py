import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session
from typing import Dict, Any
import json
import secrets 
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure Gemini API
genai.configure(api_key='')  # Replace with your API key
model = genai.GenerativeModel('gemini-pro')

class CareerEmpowermentSystem:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_career_path(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized career recommendations and advancement strategies"""
        prompt = f"""
        As an AI career advisor specialized in women's empowerment in STEM, analyze the following background and provide recommendations.
        Return the response in strict JSON format like this example:
        {{
            "career_paths": [
                {{"title": "Data Scientist", "description": "...", "growth_potential": "..."}},
                {{"title": "ML Engineer", "description": "...", "growth_potential": "..."}},
                {{"title": "Tech Lead", "description": "...", "growth_potential": "..."}}
            ],
            "leadership_development": {{
                "key_skills": ["...", "...", "..."],
                "development_plan": "..."
            }},
            "salary_insights": {{
                "salary_ranges": {{
                    "entry_level": "...",
                    "mid_level": "...",
                    "senior_level": "..."
                }},
                "negotiation_tips": ["...", "...", "..."]
            }},
            "learning_path": {{
                "courses": ["...", "...", "..."],
                "certifications": ["...", "...", "..."]
            }},
            "mentorship": {{
                "networking_groups": ["...", "...", "..."],
                "mentorship_programs": ["...", "...", "..."]
            }},
            "advancement_strategies": {{
                "short_term": ["...", "...", "..."],
                "long_term": ["...", "...", "..."]
            }},
            "resources": {{
                "organizations": ["...", "...", "..."],
                "support_networks": ["...", "...", "..."]
            }}
        }}

        Background Information:
        - Skills: {user_data['skills']}
        - Interests: {user_data['interests']}
        - Location: {user_data['location']}
        - Current Role: {user_data.get('current_role', 'Not specified')}
        - Career Goals: {user_data.get('career_goals', 'Not specified')}
        
        Ensure the response is in valid JSON format exactly matching the structure above.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            return json.loads(response_text)
        
        except Exception as e:
            # Return dummy data if the API fails
            print(f"Error generating career path: {str(e)}")
            return self._get_dummy_career_data()

    def analyze_gender_pay_gap(self, role: str, location: str) -> Dict[str, Any]:
        """Analyze industry-specific gender pay gap data"""
        prompt = f"""
        Provide data-driven insights about gender pay gap for {role} in {location}.
        Return the response in strict JSON format like this example:
        {{
            "industry_salary": {{
                "average": "...",
                "range": {{
                    "min": "...",
                    "max": "..."
                }}
            }},
            "gender_pay_gap": {{
                "percentage": "...",
                "industry_comparison": "..."
            }},
            "contributing_factors": [
                "...",
                "...",
                "..."
            ],
            "negotiation_strategies": [
                "...",
                "...",
                "..."
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            return json.loads(response_text)
        
        except Exception as e:
            print(f"Error analyzing pay gap: {str(e)}")
            return self._get_dummy_pay_gap_data()

    def _get_dummy_career_data(self) -> Dict[str, Any]:
        """Return dummy data for career recommendations and advancement"""
        return {
            "career_paths": [
                {"title": "Data Scientist", "description": "Analyze data to extract insights.", "growth_potential": "High"},
                {"title": "Machine Learning Engineer", "description": "Develop ML models.", "growth_potential": "High"},
                {"title": "Technical Lead", "description": "Lead technical projects.", "growth_potential": "Moderate"}
            ],
            "leadership_development": {
                "key_skills": ["Leadership", "Strategic Thinking", "Communication"],
                "development_plan": "Participate in leadership training and workshops."
            },
            "salary_insights": {
                "salary_ranges": {
                    "entry_level": "$60,000 - $80,000",
                    "mid_level": "$80,000 - $110,000",
                    "senior_level": "$110,000 - $150,000"
                },
                "negotiation_tips": ["Research market rates", "Highlight unique skills", "Be prepared to negotiate"]
            },
            "learning_path": {
                "courses": ["Introduction to Data Science", "Advanced Machine Learning", "Project Management Essentials"],
                "certifications": ["Certified Data Scientist", "Machine Learning Specialist"]
            },
            "mentorship": {
                "networking_groups": ["Women in STEM Network", "AI Mentorship Circle"],
                "mentorship_programs": ["Women in Tech Mentorship", "Tech Career Accelerator"]
            },
            "advancement_strategies": {
                "short_term": ["Complete relevant certifications", "Build a strong network", "Seek mentorship"],
                "long_term": ["Aim for leadership roles", "Continue education in advanced topics"]
            },
            "resources": {
                "organizations": ["Society of Women Engineers", "Women in Technology International"],
                "support_networks": ["Tech Networking Events", "STEM Women Conferences"]
            }
        }

    def _get_dummy_pay_gap_data(self) -> Dict[str, Any]:
        """Return dummy data for gender pay gap analysis"""
        return {
            "industry_salary": {
                "average": "$90,000",
                "range": {
                    "min": "$70,000",
                    "max": "$120,000"
                }
            },
            "gender_pay_gap": {
                "percentage": "15%",
                "industry_comparison": "Higher than average in tech"
            },
            "contributing_factors": [
                "Historical biases",
                "Differences in negotiation outcomes",
                "Underrepresentation in senior roles"
            ],
            "negotiation_strategies": [
                "Prepare data on industry averages",
                "Emphasize unique contributions",
                "Seek mentorship on negotiation skills"
            ]
        }

career_system = CareerEmpowermentSystem()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({"error": "No data provided"}), 400
            
        career_recommendations = career_system.generate_career_path(user_data)
        pay_gap_analysis = career_system.analyze_gender_pay_gap(
            user_data.get('current_role', 'Software Engineer'),
            user_data.get('location', 'Global')
        )
        
        session['last_analysis'] = {
            'recommendations': career_recommendations,
            'pay_gap_analysis': pay_gap_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'career_path': career_recommendations,
            'pay_gap_analysis': pay_gap_analysis
        })
        
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true')
