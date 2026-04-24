import os
import subprocess
from github import Github
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai_tools import FileReadTool, FileWriterTool

milestone_title = os.getenv("MILESTONE_TITLE")
milestone_description = os.getenv("MILESTONE_DESCRIPTION")
repo_name = os.getenv("GITHUB_REPOSITORY") 
github_token = os.getenv("GITHUB_TOKEN")

cerebras_llm = LLM(
    model="llama-3.1-70b", 
    api_key=os.getenv("CEREBRAS_API_KEY"),
    base_url="https://api.cerebras.ai/v1"
)

@tool("github_pr_tool")
def github_pr_tool(branch_name: str, title: str, body: str):
    try:
        subprocess.run(["git", "config", "--global", "user.name", "AI-Developer"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "ai@example.com"], check=True)
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", title], check=True)
        subprocess.run(["git", "push", "origin", branch_name], check=True)

        g = Github(github_token)
        repo = g.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=branch_name, base="main")
        return f"Successfully created PR: {pr.html_url}"
    except Exception as e:
        return f"Error: {str(e)}"


coder = Agent(
    role='Senior NestJS Developer',
    goal=f'Implement requirements for: {milestone_title}',
    backstory='Expert in NestJS and JWT. You write clean and secure code.',
    tools=[FileReadTool(), FileWriterTool()],
    llm=cerebras_llm,
    verbose=True
)

tester = Agent(
    role='QA Engineer',
    goal='Test the implemented code and identify bugs',
    backstory='Quality expert focused on security and logic validation.',
    llm=cerebras_llm,
    verbose=True
)

reviewer = Agent(
    role='Technical Lead',
    goal='Review the code and open a Pull Request',
    backstory='Final reviewer who ensures quality before submission.',
    tools=[github_pr_tool],
    llm=cerebras_llm,
    verbose=True
)


task_coding = Task(
    description=f"Implement: {milestone_title}. Details: {milestone_description}",
    expected_output="Code files created based on the milestone requirements.",
    agent=coder
)

task_testing = Task(
    description="Analyze the code for bugs and security flaws. Provide a report.",
    expected_output="A confirmation that the code is stable.",
    agent=tester,
    context=[task_coding]
)

task_review_pr = Task(
    description="If testing passes, push the code and open a Pull Request with a summary.",
    expected_output="The URL of the created Pull Request.",
    agent=reviewer,
    context=[task_testing]
)


dev_crew = Crew(
    agents=[coder, tester, reviewer],
    tasks=[task_coding, task_testing, task_review_pr],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    dev_crew.kickoff()
