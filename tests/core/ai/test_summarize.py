import os
from unittest.mock import patch
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import pytest

def test_chat_open_ai_initialization():
    with patch.dict('os.environ', {'OPENAI_TOKEN': 'test_token'}):
        chat_open_ai = ChatOpenAI(temperature=0, openai_api_key=os.environ['OPENAI_TOKEN'], model_name="gpt-4-1106-preview")
        assert chat_open_ai.temperature == 0
        assert chat_open_ai.openai_api_key == 'test_token'
        assert chat_open_ai.model_name == "gpt-4-1106-preview"

def test_open_ai_embeddings_initialization():
    with patch.dict('os.environ', {'OPENAI_TOKEN': 'test_token'}):
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_TOKEN'])
        assert embeddings.openai_api_key == 'test_token'

def test_character_text_splitter_initialization():
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name="gpt-4-1106-preview")
    assert text_splitter.model_name == "gpt-4-1106-preview"

def test_load_summarize_chain():
    with patch.dict('os.environ', {'OPENAI_TOKEN': 'test_token'}):
        chat_open_ai = ChatOpenAI(temperature=0, openai_api_key=os.environ['OPENAI_TOKEN'], model_name="gpt-4-1106-preview")
        question_template = "test_template"
        question_prompt = PromptTemplate.from_template(question_template)
        chain = load_summarize_chain(llm=chat_open_ai, chain_type="stuff", prompt=question_prompt, verbose=True)
        assert chain.llm == chat_open_ai
        assert chain.chain_type == "stuff"
        assert chain.prompt == question_prompt
        assert chain.verbose == True
