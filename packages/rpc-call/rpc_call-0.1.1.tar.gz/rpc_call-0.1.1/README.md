> **Note**
> TThe main idea of the project is based on RabbitMQ RPC, so RabbitMQ must be installed. Keep it mind.

### Get started
-------------
#### *Simple RPC client using FastAPI*


#### **`server.py`**

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

```shell
$ python server.py
```

-------------
#### *Simple RPC server*

#### **`client.py`**

```python
from rpc_call.server import RPCServer

class CallbackHandler:
    def test_func(self, arg1: str) -> str:
        return "test_func rpc result"

if __name__ == "__main__":
    RPCServer(
        amqp_dsn = "<amqp://login:password@host:port/vhost>",
        queue_name = "<RabbitMQQueueName>",
        callback_handler = CallbackHandler
    )
```

```bash
$ uvicorn client:app --host 0.0.0.0 --port 8000 --reload
```
