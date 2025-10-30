# Flow Manager (Delta Capita task)

Implements the JSON flow example from the task document.

A flow has:
- `start_task`
- a list of tasks (names only)
- conditions that tell the service which task to run next based on success/failure

The service:
1. starts at `start_task`
2. runs the task from the registry
3. looks up the condition for that task
4. jumps to the next task or ends
5. returns an execution trace

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
