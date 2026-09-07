googleapiclient.errors.HttpError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/paper-analyzer./app.py", line 60, in <module>
    upload = genai.upload_file(f.name)
File "/home/adminuser/venv/lib/python3.14/site-packages/google/generativeai/files.py", line 85, in upload_file
    response = client.create_file(
        path=path, mime_type=mime_type, name=name, display_name=display_name, resumable=resumable
    )
File "/home/adminuser/venv/lib/python3.14/site-packages/google/generativeai/client.py", line 103, in create_file
    self._setup_discovery_api(metadata)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/google/generativeai/client.py", line 84, in _setup_discovery_api
    response, content = request.execute()
                        ~~~~~~~~~~~~~~~^^
File "/home/adminuser/venv/lib/python3.14/site-packages/googleapiclient/_helpers.py", line 130, in positional_wrapper
    return wrapped(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.14/site-packages/googleapiclient/http.py", line 1018, in execute
    raise HttpError(resp, content, uri=self.uri)
