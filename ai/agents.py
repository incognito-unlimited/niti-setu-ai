import pandas as pd
from groq import Groq
from typing import List, Dict
import json

class InsuranceAgent:
    def __init__(self):
        self.client = Groq()
        self.model = "llama-3.3-70b-versatile"
        
    def _process_user_data(self, data: pd.DataFrame) -> Dict:
        """
        Process user data to extract relevant features for policy recommendations
        """
        profile = {
            "age": data["age"].iloc[0],
            "income": data["income"].iloc[0],
            "occupation": data["occupation"].iloc[0],
            "family_status": data["family_status"].iloc[0],
            "existing_policies": data["existing_policies"].iloc[0] if "existing_policies" in data.columns else [],
            "risk_factors": data["risk_factors"].iloc[0] if "risk_factors" in data.columns else []
        }
        return profile

    def _create_recommendation_prompt(self, user_profile: Dict) -> str:
        """
        Create a structured prompt for the LLM based on user profile
        """
        prompt = f"""
        Based on the following user profile, recommend suitable insurance policies:
        
        Age: {user_profile['age']}
        Income: ${user_profile['income']}
        Occupation: {user_profile['occupation']}
        Family Status: {user_profile['family_status']}
        Existing Policies: {', '.join(user_profile['existing_policies'])}
        Risk Factors: {', '.join(user_profile['risk_factors'])}
        
        Provide recommendations in the following JSON format:
        {{
            "primary_recommendations": [
                {{"policy_type": "", "reason": "", "estimated_premium": "", "coverage": ""}}
            ],
            "upsell_opportunities": [
                {{"policy_type": "", "reason": "", "benefit_over_existing": ""}}
            ]
        }}
        """
        return prompt

    def get_recommendations(self, user_data: pd.DataFrame) -> Dict:
        """
        Get policy recommendations based on user data
        """
        user_profile = self._process_user_data(user_data)
        prompt = self._create_recommendation_prompt(user_profile)
        
        messages = [
            {"role": "system", "content": "You are an expert insurance advisor. Provide detailed policy recommendations based on user profiles."},
            {"role": "user", "content": prompt}
        ]
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None
        )
        
        try:
            recommendations = json.loads(completion.choices[0].message.content)
            return recommendations
        except json.JSONDecodeError:
            return {"error": "Failed to parse recommendations"}

    def fine_tune_model(self, training_data: List[Dict]):
        """
        Fine-tune the model based on historical recommendations and outcomes
        """
        # Note: Implementation would depend on Groq's fine-tuning capabilities
        # This is a placeholder for the fine-tuning logic
        pass

    def evaluate_recommendations(self, recommendations: Dict, actual_purchases: List[str]) -> float:
        """
        Evaluate the quality of recommendations based on actual user purchases
        """
        recommended_policies = [rec["policy_type"] for rec in recommendations["primary_recommendations"]]
        recommended_policies.extend([rec["policy_type"] for rec in recommendations["upsell_opportunities"]])
        
        accuracy = len(set(recommended_policies) & set(actual_purchases)) / len(recommended_policies)
        return accuracy

def load_user_data(file_path: str) -> pd.DataFrame:
    """
    Load and validate user data from uploaded file
    """
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
            
        required_columns = ["age", "income", "occupation", "family_status"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError("Missing required columns in user data")
            
        return data
    except Exception as e:
        raise Exception(f"Error loading user data: {str(e)}")
