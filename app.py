"""
    This module defines a FastAPI application that provides an HTTP API for interacting
    with a file management agent.

    To run the server, execute this script directly. The server will start on host `0.0.0.0`
    and port `8000`.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import get_file_agent

app = FastAPI()


class AgentRequest(BaseModel):
    """
    Request model for the agent endpoint.

    Attributes:
        msg (str): The command message instructing the agent on what action to perform.
        root_dir (str): The root directory path where the agent will perform file
            operations. Defaults to the current directory.
    """

    msg: str
    root_dir: str = "./"


@app.post("/agent", response_model=dict)
async def agent_endpoint(request: AgentRequest):
    """
    Endpoint for handling requests to the agent.

    Parameters:
    - request (AgentRequest): The request payload containing the following:
        - msg (str): The command message instructing the agent on what action to perform.
        - root_dir (Optional[str]): The root directory path
                                    where the agent will perform file operations.

    Returns:
    - dict: A dictionary with a single field:
        - "msg" (str): The response message indicating the outcome of the operation.

    Raises:
    - HTTPException (status_code=500): If an error occurs during command execution.
    """
    agent_executor = get_file_agent(root_dir=request.root_dir)
    try:
        response = agent_executor.invoke({"input": request.msg})
        return {"msg": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Run server on 0.0.0.0:8000
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
