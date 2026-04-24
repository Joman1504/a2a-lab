from vertexai.preview import reasoning_engines
agent = reasoning_engines.ReasoningEngine('projects/1095504584646/locations/us-central1/reasoningEngines/2667741214182211584')
response = agent.query(message_text='!summarise')
print(response)

