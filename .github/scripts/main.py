import os
import subprocess
from github import Github
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai_tools import FileReadTool, FileWriterTool

milestone_title = os.getenv("MILESTONE_TITLE", "Default Task")
milestone_description = os.getenv("MILESTONE_DESCRIPTION", "No description provided")
repo_name = os.getenv("GITHUB_REPOSITORY") 
github_token = os.getenv("GITHUB_TOKEN")

# إعداد Cerebras LLM
cerebras_llm = LLM(
    model="cerebras/llama3.3-70b",
    api_key=os.getenv("CEREBRAS_API_KEY"),
    base_url="https://api.cerebras.ai/v1"
)


@tool("github_pr_action")
def github_pr_action(branch_name: str, pr_title: str, pr_body: str):
    try:
        subprocess.run(["git", "config", "--global", "user.name", "AI-Agent"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "ai@agent.com"], check=True)
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", pr_title], check=True)
        subprocess.run(["git", "push", "origin", branch_name], check=True)

        g = Github(github_token)
        repo = g.get_repo(repo_name)
        pr = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base="main")
        
        return f"Pull Request Created: {pr.html_url}"
    except Exception as e:
        return f"Error: {str(e)}"


coder = Agent(
    role='Senior NestJS Developer',
    goal=f'Implement requirements for: {milestone_title}',
    backstory='Expert in NestJS and JWT. Writes production-ready code.',
    tools=[FileReadTool(), FileWriterTool()],
    llm=cerebras_llm,
    verbose=True
)

tester = Agent(
    role='QA Engineer',
    goal='Ensure the code is bug-free and meets security standards',
    backstory='Expert in unit and integration testing.',
    llm=cerebras_llm,
    verbose=True
)

reviewer = Agent(
    role='Technical Lead',
    goal='Review code quality and submit Pull Request',
    backstory='Ensures code follows best practices and opens the PR.',
    tools=[github_pr_action],
    llm=cerebras_llm,
    verbose=True
)


task_coding = Task(
    description=f"Task: {milestone_title}. Requirements: {milestone_description}. Implement the NestJS logic.",
    expected_output="Functional code files created.",
    agent=coder
)

task_testing = Task(
    description="Analyze the generated code for any logic errors or security flaws.",
    expected_output="A detailed test report confirming the code is ready.",
    agent=tester,
    context=[task_coding]
)

task_review_and_pr = Task(
    description="Review the code and test report. If approved, use github_pr_action to push and open a PR.",
    expected_output="URL of the created Pull Request.",
    agent=reviewer,
    context=[task_testing]
)


crew = Crew(
    agents=[coder, tester, reviewer],
    tasks=[task_coding, task_testing, task_review_and_pr],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    crew.kickoff()
