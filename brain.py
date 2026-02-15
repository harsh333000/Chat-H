import groq

client = groq.Groq(api_key="Gsk_By26GCCJxC7rcHbOZ7JNWGdyb3FYE6UiblfyMXzGVIObrZNnjO0P")

def get_ai_response(user_input):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Chat H, a powerful AGI. Answer concisely."},
                {"role": "user", "content": user_input}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"System Error: {str(e)}"

