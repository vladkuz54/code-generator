from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)


class CodeGrader(BaseModel):
    code_grader: bool = Field(
        description="Code quality grade assigned by the tester agent (True for pass, False for fail)."
    )


structured_llm_output = llm.with_structured_output(CodeGrader)

system = """You are a code auditor. Evaluate the code against the user query on:
1. Functional completeness - all requirements met
2. Correctness - no syntax/logic errors, edge cases handled
3. Architecture - follows defined patterns
4. Efficiency - no unnecessary complexity

Respond with code_grade: True if all pass, False otherwise.
"""

prompt = ChatPromptTemplate(
    [("system", system), ("human", "User query:\n{query}\n\nCode:{coder_output}")]
)

code_grader_chain = prompt | structured_llm_output
