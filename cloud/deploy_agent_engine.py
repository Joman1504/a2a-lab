# cloud/deploy_agent_engine.py
import os
import sys
import uuid
import asyncio
import vertexai
from vertexai.preview import reasoning_engines
from typing import Any, Dict

PROJECT_ID = 'a2a-agent-project-493700'
REGION     = 'us-central1'
STAGING    = f'gs://{PROJECT_ID}-a2a-staging'

# -------- A2A WRAPPER --------
# Due to issues with detecting imported modules, I decided to just move the wrapper here.
class EchoAgent:
    """Agent Engine wrapper defined in-file to ensure serialisation success."""

    def set_up(self):
        print('EchoAgent.set_up() called')
        pass

    def query(self, message_text: str, task_id: str = None) -> Dict[str, Any]:
        # Local import inside the method to resolve within the cloud runtime
        import handlers
        from types import SimpleNamespace

        # Create the A2A-compliant request structure [cite: 94]
        fake_request = SimpleNamespace(
            id=task_id or str(uuid.uuid4()),
            message=SimpleNamespace(
                role='user',
                parts=[SimpleNamespace(type='text', text=message_text)]
            ),
        )

        # Run the async handler in the sync Reasoning Engine environment 
        result_text = asyncio.run(handlers.handle_task(fake_request))

        return {
            'id':       fake_request.id,
            'status':   {'state': 'completed'},
            'artifacts':[{'parts':[{'type':'text','text':result_text}]}]
        }

# -------- DEPLOYMENT --------
def deploy():
    # Resolve absolute path to the server directory for extra_packages
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_dir = os.path.abspath(os.path.join(current_dir, '..', 'server'))
    
    # Define exactly which files we need to send
    # This prevents Dockerfiles or .venv folders from breaking the build
    handlers_path = os.path.join(server_dir, 'handlers.py')
    card_path = os.path.join(server_dir, 'agent_card.py')

    vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=STAGING)

    print("Deploying Echo Agent to Vertex AI Agent Engine...")

    # Package and deploy
    remote_agent = reasoning_engines.ReasoningEngine.create(
        EchoAgent(),
        requirements=[
            'google-cloud-aiplatform==1.139.0',
            'cloudpickle==3.0.0',
            'fastapi==0.111.0',
            'pydantic==2.9.0',
        ],
        # Add handlers.py and agent_card.py as extra_packages
        extra_packages=[handlers_path, card_path], 
        display_name='Echo_A2A_Final',
    )

    print('Deployed! Resource name:', remote_agent.resource_name)
    print('Engine ID:', remote_agent.resource_name.split("/")[-1])

if __name__ == "__main__":
    deploy()