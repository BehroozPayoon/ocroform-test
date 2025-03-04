from pydantic import BaseModel


class SingleFetchRequest(BaseModel):

    source_file: str
