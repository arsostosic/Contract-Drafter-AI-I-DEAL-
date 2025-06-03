from typing import Optional
from pinecone_plugins.assistant.data.core.client.model.search_completions import SearchCompletions as ChatCompletionsRequest
from pinecone_plugins.assistant.data.core.client.model.assistant_file_model import AssistantFileModel as OpenAIFileModel

class FileModel:
    def __init__(self, file_model: Optional[OpenAIFileModel] = None, data: dict[str, any] = None):
        if data:
            self.data_init(data)
        else:
            self.file_model_init(file_model)

    def data_init(self, data: dict[str, any]):
        self.data = data
        self.name = data.get("name")
        self.id = data.get("id")
        self.metadata = data.get("metadata")
        self.created_on = data.get("created_on")
        self.updated_on = data.get("updated_on")
        self.status = data.get("status")
        self.percent_done = data.get("percent_done")
        self.signed_url = data.get("signed_url")
    
    def file_model_init(self, file_model: OpenAIFileModel):
        self.file_model = file_model
        self.name = self.file_model.name
        self.created_on = self.file_model.created_on
        self.updated_on = self.file_model.updated_on
        self.metadata = self.file_model.metadata
        self.status = self.file_model.status
        self.mime_type = self.file_model.mime_type

    def __str__(self):
        return str(self.file_model)
    
    def __repr__(self):
        return repr(self.file_model)

    def __getattr__(self, attr):
        return getattr(self.file_model, attr) 
    
