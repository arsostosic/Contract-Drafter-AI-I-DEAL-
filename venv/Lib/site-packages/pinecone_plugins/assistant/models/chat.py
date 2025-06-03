from typing import Optional

from pinecone_plugins.assistant.models.file_model import FileModel


class Message:
    def __init__(self, data: Optional[dict[str, any]] = None, **kwargs) -> None:
        if data:
            self.role = data.get("role")
            self.content = data.get("content")
        else:
            self.role = kwargs.get("role", "user")
            self.content = kwargs.get("content")
    
    def __str__(self) -> str:
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))

    def __getattr__(self, attr):
        return vars(self).get(attr)
                       
class ChatResultModel:
    def __init__(self, data):
        self.data = data
        self.id = data.get("id")
        self.choices = [StreamCompletionChoice(data=choice_data) for choice_data in data.get("choices", [])]
        self.model = data.get("model")

    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return repr(self.data)

    def __getattr__(self, attr):
        return getattr(self.data, attr)

class StreamingChatCompletionResultModel:
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.id = data.get("id")
        self.choices = [StreamCompletionChoice(data=choice_data) for choice_data in data.get("choices", [])]
        self.model = data.get("model")
    
    def __str__(self) -> str:
        return str(self.data)



class StreamCompletionChoice: 
    def __init__(self, data: dict[str, any]) -> None:
        self.index = data.get("index")
        self.delta = Message(data=data.get("delta"))
        self.finish_reason = data.get("finish_reason")
    
    def __str__(self) -> str:
        return str(vars(self))
    

class CompletionChoice: 
    def __init__(self, data: dict[str, any]) -> None:
        self.index = data.get("index")
        self.message = Message(data=data.get("message"))
        self.finish_reason = data.get("finish_reason")
    
    def __str__(self) -> str:
        return str(vars(self))


"""
Define the data model for the chat streaming response
"""
class StreamChatResultModelMessageStart:
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.type = data.get("type")
        self.model = data.get("model")
        self.role = data.get("role")
    
    def __str__(self) -> str:
        return str(self.data)

class StreamChatResultModelContentDelta:
    class MessageDelta:
        def __init__(self, data: dict[str, any]) -> None:
            self.content = data.get("content")
        
        def __str__(self) -> str:
            return str(vars(self))
        
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.type = data.get("type")
        self.id = data.get("id")
        self.model = data.get("model")
        self.delta = StreamChatResultModelContentDelta.MessageDelta(data.get("delta"))

    def __str__(self) -> str:
        return str(self.data)

class Reference:
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.pages = data.get("pages")
        self.file = FileModel(data=data.get("file"))

    def __str__(self) -> str:
        return str(self.data)

class Citation:
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.position = data.get("position")
        self.references = [Reference(data=reference_data) for reference_data in data.get("references", [])]

    def __str__(self) -> str:
        return str(self.data)

class StreamChatResultModelCitation:
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.type = data.get("type")
        self.id = data.get("id")
        self.model = data.get("model")
        self.citation = Citation(data.get("citation"))
    
    def __str__(self) -> str:
        return str(self.data)
        

class StreamChatResultModelMessageEnd:
    def __init__(self, data: dict[str, any]) -> None:
        self.data = data
        self.type = data.get("type")
        self.model = data.get("model")
        self.id = data.get("id")
        if data.get("usage"):
            self.usage = Usage(data.get("usage", {}))
    
    def __str__(self) -> str:
        return str(self.data)

class Usage:
    def __init__(self, data: dict[str, any] = {}) -> None:
        self.data = data
        self.prompt_tokens = data.get("prompt_tokens", 0)
        self.completion_tokens = data.get("completion_tokens", 0)
        self.total_tokens = data.get("total_tokens", 0)
        
    def __str__(self) -> str:
        return str(self.data)
