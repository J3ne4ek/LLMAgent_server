"""
    This module contains unit tests for the FastAPI application defined in the main module.
"""

import os

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


async def send_agent_request(msg, root_dir="./"):
    """
    Sends a request to the agent endpoint.

    Args:
        msg (str): The command message to send to the agent.
        root_dir (str): The root directory path for the agent's file operations.
                         Defaults to the current directory ("./").

    Returns:
        Response: The response object from the HTTP POST request to the agent endpoint.
    """
    return client.post("/agent", json={"msg": msg, "root_dir": root_dir})


@pytest.mark.asyncio
async def test_create_folder():
    """
    Tests the creation of a folder.

    This test sends a request to create a folder and checks if the folder
    was created successfully in the file system.
    """
    folder_name = "test_folder"
    response = await send_agent_request(f"Create a folder named {folder_name}")

    assert response.status_code == 200
    assert os.path.isdir(folder_name), "Folder was not created successfully."

    os.rmdir(folder_name)


@pytest.mark.asyncio
async def test_create_file():
    """
    Tests the creation of a file.

    This test sends a request to create a file and checks if the file
    was created successfully in the file system.
    """
    file_name = "test_file.txt"
    response = await send_agent_request(f"Create a file named {file_name}")

    assert response.status_code == 200
    assert os.path.isfile(file_name), "File was not created successfully."

    os.remove(file_name)


@pytest.mark.asyncio
async def test_create_file_and_folder():
    """
    Tests the creation of a file within a folder.

    This test sends a request to create a file in a specified directory,
    ensuring the directory is created if it doesn't already exist.
    """
    test_dir = "test_dir"
    file_name = "test_file.txt"
    response = await send_agent_request(
        f"Create a file named {file_name} in {test_dir}. "
        f"If {test_dir} doesn't exist, create it."
    )

    assert response.status_code == 200
    assert os.path.isdir(test_dir), "Folder was not created successfully."
    assert os.path.isfile(
        os.path.join(test_dir, file_name)
    ), "File was not created successfully."

    os.remove(os.path.join(test_dir, file_name))
    os.rmdir(test_dir)


@pytest.mark.asyncio
async def test_rename_file():
    """
    Tests renaming a file.

    This test sends a request to rename a specified file and checks if
    the old file name no longer exists while the new file name does.
    """
    file_name = "old_file.txt"
    new_file_name = "new_file.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write("This is a test file.")

    response = await send_agent_request(f"Rename file {file_name} to {new_file_name}")

    assert response.status_code == 200
    assert not os.path.isfile(file_name)
    assert os.path.isfile(new_file_name)

    os.remove(new_file_name)


@pytest.mark.asyncio
async def test_list_files_in_directory():
    """
    Tests listing files in the current directory.

    This test creates several test files and sends a request to list
    all `.txt` files, verifying that the correct files are listed in
    the response.
    """
    file_names = ["file1.txt", "file2.txt", "file3.log"]
    for name in file_names:
        with open(name, "w", encoding="utf-8") as f:
            f.write("This is a test file.")

    response = await send_agent_request("List all .txt files")

    assert response.status_code == 200
    assert "file1.txt" in response.json()["msg"]
    assert "file2.txt" in response.json()["msg"]
    assert "file3.log" not in response.json()["msg"]

    for name in file_names:
        os.remove(name)


@pytest.mark.asyncio
async def test_change_file_extension():
    """
    Tests changing the extension of specific files in a directory.

    This test creates files in a test directory and sends a request
    to change the extension of files that contain the word 'log' in their names
    from `.txt` to `.log`.
    """
    test_dir = "test_dir"
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    file_names = ["file1_log.txt", "log.txt", "file2.txt", "file3.log"]
    new_file_names = ["file1_log.log", "log.log", "file2.txt", "file3.log"]
    for name in file_names:
        with open(os.path.join(test_dir, name), "w", encoding="utf-8") as f:
            f.write("This is a test file.")

    response = await send_agent_request(
        f"I want to find all files in directory {test_dir} with .txt extension. "
        f"Then for those of these files which contain at least 1 word log, "
        f"change their extension to .log"
    )

    print(response.json())

    assert response.status_code == 200
    for name in new_file_names:
        assert os.path.isfile(
            os.path.join(test_dir, name)
        ), f"File {name} does not exist."

    for name in file_names:
        if name not in new_file_names:
            assert not os.path.isfile(os.path.join(test_dir, name))

    for name in new_file_names:
        os.remove(os.path.join(test_dir, name))
    os.rmdir(test_dir)
