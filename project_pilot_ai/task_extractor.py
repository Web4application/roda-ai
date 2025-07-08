from typing import List, Dict
import openai
import os

class TaskExtractor:
    def __init__(self, model="gpt-4"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def extract_tasks(self, transcript: str) -> List[Dict]:
        prompt = f"""
        Extract action items from the following meeting transcript. Include task, deadline (if any), and owner.
        Mark missing fields as 'TBD'.

        Transcript:
        {transcript}
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        output = response['choices'][0]['message']['content']
        return self._parse_output(output)

    def _parse_output(self, raw_text: str) -> List[Dict]:
        tasks = []
        for line in raw_text.splitlines():
            if "-" in line:
                parts = line.strip("- ").split(" | ")
                if len(parts) == 3:
                    tasks.append({
                        "task": parts[0].strip(),
                        "owner": parts[1].strip(),
                        "deadline": parts[2].strip()
                    })
        return tasks
