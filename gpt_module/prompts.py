from langchain.prompts import PromptTemplate


question_template = (
    "You are an expert in summarizing conversations in public text chats.",
    "Your goal is to create a summary of the conversation and extract main topics that were discussed, who started topic and who participated in this topic conversation.",
    "Below you can find the transcript of the conversation:",
    "--------",
    "{text}",
    "--------",
    "",
    "SUMMARY AND TOPIC BULLET LIST WITH THEIR AUTHORS AND PARTICIPANTS:",
)

question_prompt = PromptTemplate.from_template('\n'.join(question_template))
