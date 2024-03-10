from gentopia.prompt import PromptTemplate
from gentopia.tools import GoogleSearch 

VanillaPrompt = PromptTemplate(
    input_variables=["instruction"],
    template=lambda args: GoogleSearch(args["[instruction]"])if "tell me about" in args["instruction"].lower() else args["instruction"]
)

FewShotVanillaPrompt = PromptTemplate(
    input_variables=["instruction", "fewshot"],
    template=lambda args: args["fewshot"] + "\n\n" + GoogleSearch(args["instruction"]) if "tell me about" in args["instruction"].lower() else args["instruction"]
)
