from gentopia.prompt import PromptTemplate
from gentopia import Google_Search 

VanillaPrompt = PromptTemplate(
    input_variables=["instruction"],
    template=lambda args: Google_Search(args["[instruction]"])if "tell me about" in args["instruction"].lower() else args["instruction"]
)

FewShotVanillaPrompt = PromptTemplate(
    input_variables=["instruction", "fewshot"],
    template=lambda args: args["fewshot"] + "\n\n" + gentopia_search(args["instruction"]) if "tell me about" in args["instruction"].lower() else args["instruction"]
)
