
import openai

def analyze_cli_output(cli_text, api_key, project_id):
    if not cli_text.strip():
        return "No input provided."

    client = openai.OpenAI(api_key=api_key, project=project_id)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior network engineer. Analyze the following CLI output or configuration and explain its purpose, any issues, and suggest best practices."},
            {"role": "user", "content": cli_text}
        ]
    )
    return response.choices[0].message.content

def generate_config_from_intent(intent, api_key, project_id):
    if not intent.strip():
        return "No intent provided."

    client = openai.OpenAI(api_key=api_key, project=project_id)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior Cisco network engineer. Generate a best-practice Cisco IOS configuration based on the user's intent."},
            {"role": "user", "content": intent}
        ]
    )
    return response.choices[0].message.content
