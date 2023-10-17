from typing import List

from gpt_module.misc.settings import GptSettings


def generate_summary(conversation: List[str]) -> str:

    gpt = GptSettings()

    conversation = '\n\n'.join(conversation)
    documents = gpt.text_splitter.create_documents(gpt.text_splitter.split_text(conversation))

    generated_summary: str = gpt.chain.run(documents)

    return generated_summary
