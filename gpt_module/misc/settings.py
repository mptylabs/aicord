from langchain.chains.summarize import load_summarize_chain, BaseCombineDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, TS

from configs.config import settings
from gpt_module.prompts import question_prompt


class GptSettings:
    def __init__(self):
        openai_api_key = settings.openai_token
        model_name = "gpt-3.5-turbo-16k"
        llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        self.text_splitter: TS = CharacterTextSplitter.from_tiktoken_encoder(
            model_name=model_name,
            # chunk_size=1000,
            # chunk_overlap=200,
        )

        self.chain: BaseCombineDocumentsChain = (load_summarize_chain(
            llm,
            chain_type="stuff",
            prompt=question_prompt,
            # chain_type="refine",
            # question_prompt=question_prompt,
            # refine_prompt=refine_prompt,
            verbose=True)
        )
