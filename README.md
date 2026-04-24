# a2a-lab
A repo for a CS4680 assignment

Cloud Run service URL: https://echo-a2a-agent-1095504584646.us-central1.run.app

---

# Required dependencies:
    Python 3.10+
    pip and venv
    Docker Desktop
    Google Cloud CLI
    Google Cloud projcet with billing enabled
    APIs enabled: Cloud Run, Artifact Registry, Vertex AI

# Setup:
    python -m venv .venv
    source .venv/bin/activate              # Windows: .venv\Scripts\activate
    pip install fastapi uvicorn httpx pydantic google-cloud-aiplatform
    pip install google-auth requests

---

# Running Locally
    Start the A2A server
```bash
# cd to /server
uvicorn main:app --reload --port 8000
```
    Verify it's running:
```bash
# Agent Card
curl http://localhost:8000/.well-known/agent.json

# Health check
curl http://localhost:8000/health

# Send a task
curl -X POST http://localhost:8000/tasks/send \
  -H "Content-Type: application/json" \
  -d '{"id":"t1","message":{"role":"user","parts":[{"type":"text","text":"Hello A2A"}]}}'
```

---

# Run the Client Demo (Locally)
```bash
python client/demo.py
```

---

# Deploy to Cloud Run
Fill in your `PROJECT_ID` in `cloud/deploy_cloud_run.sh`, then:
```bash
bash cloud/deploy_cloud_run.sh
```
The script will print the Service URL at the end. Point the client at it:
```python
# In client/demo.py
client = A2AClient('https://<SERVICE_URL>')
```
Run the demo against the cloud:
```bash
python client/demo.py
```
My Cloud Run Service URL:
```
https://echo-a2a-agent-1095504584646.us-central1.run.app
```

---

# Deploy to Vertex AI Agent Engine
Create the GCS staging bucket:
```bash
gsutil mb -l us-central1 gs://<your-project-id>-a2a-staging
```
Fill in your `PROJECT_ID` in `cloud/deploy_agent_engine.py`, then:
```bash
python cloud/deploy_agent_engine.py
```
The script prints the Engine ID on success. Query the deployed agent:
```python
from vertexai import agent_engines

agent = agent_engines.AgentEngine('projects/<PROJECT>/locations/us-central1/reasoningEngines/<ENGINE_ID>')
response = agent.query(message_text='Hello from Agent Engine!')
print(response)
```

---

# Cleanup
Delete Cloud Run service when done to avoid charges:
```bash
gcloud run services delete echo-a2a-agent --region=us-central1
```
Delete the Agent Engine deployment:
```bash
from vertexai import agent_engines
agent = agent_engines.AgentEngine('projects/.../reasoningEngines/<ENGINE_ID>')
agent.delete()
```

---