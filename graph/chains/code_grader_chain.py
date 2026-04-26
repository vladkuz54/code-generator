from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

llm = ChatOpenAI(model="gpt-4o", temperature=0)


class CodeGrader(BaseModel):
    code_grader: bool = Field(
        description="Code quality grade assigned by the tester agent (True for pass, False for fail)."
    )


structured_llm_output = llm.with_structured_output(CodeGrader)

system = """
Role: You are a Senior QA Engineer and Technical Auditor specializing in Python automation and white-box testing.

Objective: Audit the provided Code against the Original User Query. You must determine if the code is functionally complete, bug-free, and architecturally sound.

Evaluation Criteria:

Functional Alignment: Does the code solve every requirement mentioned in the Original User Query?

Logic and Edge Cases: Are there syntax errors, logical fallacies, or unhandled edge cases (e.g., null inputs, empty strings, connection timeouts)?

Architectural Compliance: Does the implementation respect the modules and patterns defined by the Architect?

Performance: Is the implementation efficient (e.g., O(n) complexity vs. unnecessary nested loops)?

Decision Logic:

If the code passes all criteria, respond with code_grade: True and code_bug_report: None.
If the code fails any criterion, respond with code_grade: False and provide a detailed code_bug_report outlining the specific issues found.
"""

prompt = ChatPromptTemplate(
    [("system", system), ("human", "User query:\n{query}\n\nCode:{coder_output}")]
)

code_grader_chain = prompt | structured_llm_output
