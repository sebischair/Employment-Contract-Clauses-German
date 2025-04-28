from helper import llm
from helper import files

def addAnswer(clause):
    answer = llm.getAnswer(files.readText("prompts/system_minimal"), files.readText("prompts/user").replace("###content###", clause["content"]), False)
    clause["pred_label"] = answer["result"]
    clause["pred_explanation"] = answer["explanation"]
    return clause
