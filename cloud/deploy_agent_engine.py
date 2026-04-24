# cloud/deploy_agent_engine.py
import vertexai
from vertexai.preview import reasoning_engines
import sys, os, uuid, asyncio

PROJECT_ID = 'a2a-agent-project-493700'
REGION     = 'us-central1'
STAGING    = f'gs://{PROJECT_ID}-a2a-staging'

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=STAGING)

# -------- Due to issues pickling the wrapper, I had to move EchoAgent here with its own handle_task() -------------------------------- #
class EchoAgent:
    """Agent Engine wrapper for the Echo A2A Agent."""

    def set_up(self):
        print('EchoAgent.set_up() called')

    def query(self, *, task_id: str = None, message_text: str) -> dict:
        task_id = task_id or str(uuid.uuid4())

        # Inline the handler logic — no external imports needed
        if message_text.startswith('!summarise'):
            result_text = 'This is a mock one-sentence summary.'
        else:
            result_text = message_text

        return {
            'id':        task_id,
            'status':    {'state': 'completed'},
            'artifacts': [{'parts': [{'type': 'text', 'text': result_text}]}]
        }

remote_agent = reasoning_engines.ReasoningEngine.create(
    EchoAgent(),
    requirements=[
        "google-cloud-aiplatform==1.148.1"
    ],
    display_name='Echo A2A Agent',
    description='A2A Lab — Echo Agent on Agent Engine',
    gcs_dir_name=STAGING,
)

print('Deployed! Resource name:', remote_agent.resource_name)
print('Engine ID:', remote_agent.resource_name.split('/')[-1])