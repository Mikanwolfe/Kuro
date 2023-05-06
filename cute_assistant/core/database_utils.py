from typing import Any, Dict
import requests
import os
import shutil
import pprint
import secrets

# Source: https://betterprogramming.pub/build-a-question-answering-app-using-pinecone-and-python-1d624c5818bf
SEARCH_TOP_K = 10
db_bearer_token = None

def upsert_file(directory: str):
    """
    Upload all files under a directory to the vector database.
    """
    url = "http://localhost:8000/upsert-file"
    headers = {"Authorization": "Bearer " + db_bearer_token}
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_path = os.path.join(directory, filename)
            with open(file_path, "rb") as f:
                file_content = f.read()
                files.append(("file", (filename, file_content, "text/plain")))
            response = requests.post(url,
                                     headers=headers,
                                     files=files,
                                     timeout=600)
            if response.status_code == 200:
                print(filename + " uploaded successfully.")
            else:
                print(
                    f"Error: {response.status_code} {response.content} for uploading "
                    + filename)


def upsert_texts(content: list):
    """
    Upload one piece of text to the database.
    """
    url = "http://localhost:8000/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + db_bearer_token,
    }

    documents = []
    for itm in content:
        documents.append(
                {
                "id": secrets.token_hex(64 // 2),
                "text": itm,
            }
        )


    data = {
        "documents": documents
    }
    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        print(" --- UPLOAD --- ")
        pprint.pprint(content)
        print(" --- END --- ")
    else:
        print(f"Error: {response.status_code} {response.content}")
    return response.status_code

def upsert(id: str, content: str):
    """
    Upload one piece of text to the database.
    """
    url = "http://localhost:8000/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + db_bearer_token,
    }

    data = {
        "documents": [{
            "id": id,
            "text": content,
        }]
    }
    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        print(" --- UPLOAD --- ")
        pprint.pprint(content)
        print(" --- END --- ")
    else:
        print(f"Error: {response.status_code} {response.content}")
    return response.status_code


def query_database(query_prompt: str) -> Dict[str, Any]:
    url = "http://localhost:8000/query"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {db_bearer_token}",
    }
    data = {"queries": [{"query": query_prompt, "top_k": SEARCH_TOP_K}]}

    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        result = response.json()
        # process the result
        return result
    else:
        raise ValueError(f"Error: {response.status_code} : {response.content}")


def delete_vectors(ids):
    url = "http://localhost:8000/delete"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {db_bearer_token}",
    }

    data = {
        "ids" : ids,
        "deleteAll": "false"
        }

    response = requests.delete(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        result = response.json()
        # process the result
        return result
    else:
        raise ValueError(f"Error: {response.status_code} : {response.content}")

if __name__ == "__main__":
    upsert_file("datastore/to_be_upserted")
    source_dir = 'datastore/to_be_upserted'
    destination_dir = 'datastore/upserted_files'

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)
        shutil.move(source_file, destination_file)
