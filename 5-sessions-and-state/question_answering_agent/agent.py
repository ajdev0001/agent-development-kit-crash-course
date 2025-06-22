from google.adk.agents import LlmAgent  # Changed import

class Question_Answering_Agent(LlmAgent):  # Changed base class
    def __init__(self, user_name, user_preferences):
        instruction = f"""
        You are a helpful assistant that answers questions about the user's preferences.
        Here is some information about the user:
        Name: {user_name}
        Preferences: {user_preferences}
        """
        super().__init__(
            name="question_answering_agent",
            model="gemini-2.5-flash",  # Now valid for LlmAgent
            description="Question answering agent",
            instruction=instruction
        )

