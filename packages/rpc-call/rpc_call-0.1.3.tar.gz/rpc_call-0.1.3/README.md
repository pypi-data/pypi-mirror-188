> **Note:**
> The main idea of the project is based on RabbitMQ RPC, so RabbitMQ must be installed. Please keep it mind.

### Get started

#### *Simple RPC client using FastAPI*
#### **`client.py`**

```python
import asyncio
from fastapi import FastAPI, Depends, status
from rpc_call.async_client import RPCClient
from rpc_call.types import Task, TaskResult

app = FastAPI()

async def rpc_connection() -> RPCClient:
    return await RPCClient(
        amqp_dsn = "<amqp://login:password@host:port/vhost>",
        queue_name = "<RabbitMQQueueName>"
    ).connect()

@app.post("/RPCEndpoint", response_model=TaskResult)
async def read_users(task: Task, rpc_conn: RPCClient = Depends(rpc_connection)) -> TaskResult:
    task_result = await rpc_conn.call(task)
    return task_result
```
```bash
$ uvicorn client:app --host 0.0.0.0 --port 8000 --reload
```

#### *Simple RPC server*

#### **`server.py`**

```python
from rpc_call.server import RPCServer

class CallbackHandler:
    def test_func(self, arg: str) -> str:
        return f"test_func('{arg}') call result"

if __name__ == "__main__":
    RPCServer(
        amqp_dsn = "<amqp://login:password@host:port/vhost>",
        queue_name = "<RabbitMQQueueName>",
        callback_handler = CallbackHandler
    )
```
```shell
$ python server.py
```

### Usage

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/RPCEndpoint' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "procedure": "test_func",
  "kwargs": {"arg": "Hello world!"}
}'
```
And the response will be:
```json
{
  "status_code": 200,
  "result": {
    "test_func": "test_func('Hello world!') call result"
  }
}
```

---
So now, with this elegant and simple library, you can call your code remotely! 👏
Good luck! 😉


