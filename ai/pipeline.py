# Initialize the agent
agent = InsuranceAgent()

# Load user data
user_data = load_user_data("user_profile.csv")

# Get recommendations
recommendations = agent.get_recommendations(user_data)

# Evaluate recommendations (if you have actual purchase data)
actual_purchases = ["life_insurance", "health_insurance"]
accuracy = agent.evaluate_recommendations(recommendations, actual_purchases)
