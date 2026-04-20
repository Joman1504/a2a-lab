from vertexai.preview import reasoning_engines
agent = reasoning_engines.ReasoningEngine('projects/1095504584646/locations/us-central1/reasoningEngines/8857551873909981184')
response = agent.query(message_text='Hello from Agent Engine!')
print(response)

