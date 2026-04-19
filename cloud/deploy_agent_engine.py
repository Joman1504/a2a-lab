# cloud/deploy_agent_engine.py
import vertexai
from vertexai.preview import reasoning_engines
import sys, os

PROJECT_ID = 'a2a-agent-project-493700'
REGION = 'us-central1'
STAGING = f"gs://{PROJECT_ID}-a2a-staging"

# # Add server/ to path so imports resolve
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))
# from agent_engine_wrapper import EchoAgent

# Calculate the path to the wrapper file
current_dir = os.path.dirname(os.path.abspath(__file__))
wrapper_file = os.path.abspath(os.path.join(current_dir, '..', 'server', 'agent_engine_wrapper.py'))
# Then add server/ to path so imports resolve
sys.path.insert(0, os.path.join(current_dir, '..', 'server'))
from agent_engine_wrapper import EchoAgent

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=STAGING)

# Package and deploy
remote_agent = reasoning_engines.ReasoningEngine.create(
    EchoAgent(),
    requirements=[
        'google-cloud-aiplatform[reasoningengine,langchain]',
        'fastapi==0.136.0',
        'uvicorn==0.44.0',
        'pydantic==2.13.2',
    ],
    # Add wrapper file
    extra_packages=[wrapper_file],
    display_name='Echo A2A Agent',
    description='A2A Lab — Echo Agent on Agent Engine',
    gcs_dir_name=STAGING,
)
print('Deployed! Resource name:', remote_agent.resource_name)
print('Engine ID:', remote_agent.resource_name.split('/')[-1])