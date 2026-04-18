# client/demo.py
from client import A2AClient

AGENT_URL = "http://127.0.0.1:8000"

def main():
    with A2AClient(AGENT_URL) as client:
        # Fetch agent card
        card = client.fetch_agent_card()

        print("Agent Name:", card.get("name"))

        # Print skills
        skills = client.get_skills()
        print("Skills:")
        for skill in skills:
            print(f"- {skill['name']} ({skill['id']})")

        # Send a task
        response = client.send_task("Hello from the client!")

        # Extract and print result
        result_text = client.extract_text(response)
        print("Response:", result_text)

if __name__ == "__main__":
    main()