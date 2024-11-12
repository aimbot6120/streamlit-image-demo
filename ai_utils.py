import base64
from groq import Groq
import os

class ImageAnalyzer:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.llama_3_2_vision_11b = 'llama-3.2-11b-vision-preview'
        self.llama32_model = 'llama-3.2-3b-preview'
    
    def encode_image(self, image_file):
        """Encode image file to base64."""
        return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_image(self, image_bytes, prompt):
        """Analyze image using the Groq API."""
        base64_image = self.encode_image(image_bytes)
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model=self.llama_3_2_vision_11b
        )
        
        return chat_completion.choices[0].message.content