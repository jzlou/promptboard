import requests
from datetime import datetime
from config import OPENROUTER_API_KEY

def call_openrouter_api(prompt, model="google/gemini-flash-1.5"):
    url = "https://openrouter.ai/api/v1"  # Replace with the actual endpoint
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "model": model,
    }
    data = {
        "messages": prompt,
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        raise Exception(f"Error: {response.status_code}, Message: {response.text}")

class DisplayPromptEngine:
    def __init__(self):
        self.base_system_prompt = """You are a curator of concise, meaningful information for a split-flap display board - similar to those seen in train stations. Your purpose is to generate content that is both intellectually engaging and visually suited for this format.

Key Principles:
1. Intellectual Depth: While space is limited, prioritize substance over superficiality
2. Visual Clarity: Information should be structured to work with the physical limitations of split-flap displays
3. Timeless Value: Focus on insights and information that remain relevant beyond the immediate moment

Content Guidelines:
- Avoid clickbait language or sensationalism
- No rhetorical questions or "Did you know?" setups
- Use clear, direct statements
- Prioritize precision over personality
- When sharing facts, focus on meaningful implications over mere curiosity
- For news, emphasize lasting significance over temporary buzz

Display Constraints:
- Exactly {chars_per_line} characters per line (including spaces)
- Exactly {max_lines} lines
- Each message must be complete and self-contained
- Consider the physical nature of split-flap displays - text should read naturally when flipping

Response Format:
- Provide exactly {max_lines} lines of text
- Each line must be exactly {chars_per_line} characters (pad with spaces if needed)
- Use line breaks where text should split across display lines

Today's context: {current_date}
Current time: {current_time}
Content type: {content_type}"""

        self.content_type_prompts = {
            "insight": """Share an insight about the topic that reveals a deeper understanding or unexpected connection. Focus on principles, patterns, or relationships that aren't immediately obvious but are intellectually valuable.

Example structure:
- Identify a core principle or pattern
- Express it in clear, concrete terms
- Support with specific details
- Conclude with broader implication""",

            "fact": """Share a specific, concrete fact that illuminates a broader understanding of the topic. The fact should serve as a window into a larger principle or understanding.

Example structure:
- Lead with the most specific, concrete element
- Connect to broader significance
- Include scale or context
- Frame the larger implication""",

            "update": """Provide a status update that captures meaningful progress or change in the topic area. Focus on developments that indicate significant trends or milestones.

Example structure:
- Lead with the concrete change or development
- Emphasize what makes it significant
- Provide relevant context
- Connect to broader trends"""
        }

    def generate_prompt(self, 
                        topic: str,
                        content_type: str,
                        chars_per_line: int = 50,
                        max_lines: int = 5) -> str:
        """
        Generate a complete system and user prompt for the LLM.
        
        Args:
            topic: The specific topic to address
            content_type: Type of content to generate (insight/fact/update)
            chars_per_line: Maximum characters per line
            max_lines: Maximum number of lines
        """
        current_time = datetime.now()
        
        # Format the base system prompt
        system_prompt = self.base_system_prompt.format(
            chars_per_line=chars_per_line,
            max_lines=max_lines,
            current_date=current_time.strftime("%Y-%m-%d"),
            current_time=current_time.strftime("%H:%M"),
            content_type=content_type
        )
        
        # Add content type specific instructions
        content_type_prompt = self.content_type_prompts[content_type]
        system_prompt += f"\n\n{content_type_prompt}"
        
        # Add example of correctly formatted output
        system_prompt += "\n\nExample of correctly formatted output:"
        for i in range(max_lines):
            system_prompt += f"\n{'X' * chars_per_line}"
        
        return [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Generate display text about {topic} following all provided guidelines and constraints."
            }
        ]

# Example usage:
if __name__ == "__main__":
    engine = DisplayPromptEngine()
    
    # Example: Generate a system prompt for an insight about quantum computing
    prompt = engine.generate_prompt(
        topic="quantum computing",
        content_type="insight",
        chars_per_line=50,
        max_lines=5
    )
    
    print("Prompt:")
    print("-" * 50)
    print(prompt)