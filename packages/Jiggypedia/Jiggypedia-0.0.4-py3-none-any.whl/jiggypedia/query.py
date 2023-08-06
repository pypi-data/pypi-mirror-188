"""
Client library for Jiggypedia Search API.
"""

import os
from typing import Optional, List
from pydantic import BaseModel, Field
import enum

from .jiggy_session import ClientError, ServerError, jiggysession



class EmbeddingModel(str, enum.Enum):
    """
    List of supported embedding models
    """
    ada002 = 'text-embedding-ada-002'
    multi_qa_mpnet_base_cos_v1 = 'multi-qa-mpnet-base-cos-v1'


class Encoder(str, enum.Enum):
    """
    List of supported encoders/tokenizers for counting response text tokens.
    """
    cl100k_base = 'cl100k_base'   #  used by text-embedding-ada-002
    gpt3        = 'gpt3'          #  GPT3 encoder
    gpt2        = 'gpt2'          #  same as gpt3



class QueryResponse(BaseModel):
    """
    The an individual item response to a query.
    """
    text:        str             = Field(description="The response text that matched the query text.")
    distance:    float           = Field(description="The cosine distance of the reponse text from query text.")
    name:        Optional[str]   = Field(description="Any short name or title that was associated with the response text.")
    token_count: int             = Field(description="The number of tokens in 'text' as determined by the specified encoder.")
    url:         str             = Field(description="An external url that provided the original content for this text.")
    uri:         str             = Field(description="The Jiggypedia internal URI for this response. Can be used in the future to retrieve more details about this response.")

    def __str__(self):
        return f"{self.text}"

    def __repr__(self) -> str:
        dtext = self.text.replace('\n', ' ')
        if len(dtext) > 100:
            dtext = dtext[:100] + '...'
        return f'({self.distance:0.3f}) #{self.token_count:4}  {self.name:20} {dtext}'


class QueryRequest(BaseModel):
    """
    The parameters for Jiggypedia search API.
    """
    query:                  str                       = Field(description="The query text with which to search.")
    k:                      Optional[int]             = Field(default=10, ge=1, le=200, description="TThe number of documents to query prior to response chunking.")
    chunk_embedding_model:  EmbeddingModel            = Field(default=EmbeddingModel.multi_qa_mpnet_base_cos_v1, 
                                                              description="The embedding model to use to chunk and filter the response text.")    
    encoder:                Optional[Encoder]         = Field(default=Encoder.gpt3, 
                                                              description="The encoder to use for counting response chunk text tokens.  This should be the encoder the user or downstream model will use to subsequently tokenize the response text.")                                                               
    max_item_tokens:        Optional[int]             = Field(default=500,   ge=64, le=8191,
                                                              description="Limit individual response chunk items to approximately this many tokens as tokenized by the specified encoder.")
    max_total_tokens:       Optional[int]             = Field(default=524288, ge=64, le=524288, description="Limit total response chunks to this many tokens as tokenized by the specified encoder.")

    def search(self) -> List[QueryResponse]:
        return search(**self.dict())



def search(query:                 str,
           k:                     int=10,
           max_item_tokens:       int=500,
           max_total_tokens:      int=524288,
           chunk_embedding_model: EmbeddingModel=EmbeddingModel.multi_qa_mpnet_base_cos_v1) -> List[QueryResponse]:
    """
    Search a Jiggypedia for the given query , returning a list of responses.
    """
    qr = QueryRequest(**locals())
    resp = jiggysession.get('/search', model=qr)
    return [QueryResponse(**i) for i in resp.json()]
    
