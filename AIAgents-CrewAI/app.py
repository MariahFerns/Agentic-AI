
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
from crewai import Agent, Task, Crew, Process

from langchain.llms import OpenAI
import os



def get_blog(api_key):

    
    # 3. Define you agents

    # Agent 1 - Researcher
    researcher = Agent(
        role = 'Senior Research Analyst',
        goal = 'Uncover cutting-edge advancements in the field of AI and Data Science',
        backstory = 'You work at a leading Tech company. Your expertise lies in identifying emerging trends',
        verbose = True,
        tools = [search_tool],
        allow_delegation = False,
        llm = OpenAI(openai_api_key=api_key)
    )

    # Agent 2 - Content Writer
    writer = Agent(
        role = 'Tech Content Strategist',
        goal = 'Craft compelling content on Tech advancements',
        backstory = '''You are a renowned Content Strategist known for your insightful and innovative articles.
        You transform complex concepts into compelling narratives''',
        verbose = True,
        allow_delegation = True,
        llm = OpenAI(openai_api_key=api_key)
    )

    # 4. Create Tasks for your agents

    task1 = Task(
        description = '''Conduct a comprehensive analysis of the latest advancements in AI in 2024.
        Identify key trends, breakthrough technologies and potential industry impacts''',
        expected_output = 'Full analysis report in bullet points',
        agent = researcher
    )

    task2 = Task(
        description = '''Using the provided analysis, develop an engaging blog post that highlights
        the most significant AI advancements. Your post should be engaging, informative yet accessible,
        catering to a tech-savvy audience. Make it sound cool, avoid complex words and jargon so it doesn't sound like AI.''',
        expected_output = 'Full blog post of at least 4 paragraphs',
        agent = writer
    )

    # 5. Instantiate your crew

    crew = Crew(
        agents = [researcher, writer],
        tasks = [task1, task2],
        verbose = 2 # can be 1 or 2 for different logging levels
    )
    
    
    # 6. CREW in action
    response = crew.kickoff()
    return response
    
    

# 7. Create the Streamlit UI (Optional)

import streamlit as st

st.title('🔖Crew AI - Using agents for creative writing')

st.write('''We use 2 agents: Researcher & Writer to create a blog post on the lastest tech advancement in AI in 2024.
The researcher does the analysis using a search engine and passes his observations to the content writer who comes up
with an engaging blog post.''')


# Form to take API key and get response
result=[]
with st.form('myform', clear_on_submit=True):
    # get api key
    api_key = st.text_input('Enter OpenAI API key:', type='password')
    # click submit button
    submit = st.form_submit_button('Submit')
    # check if submit button is clicked and openai api key is valid
    if (submit and api_key.startswith('sk-')):
        with st.spinner('Generating blog post on AI tech advancements in 2024...'):
            response = get_blog(api_key)
            # appending response to a list that allows storing the response that can be queried later by the user
            result.append(response) 
            del api_key
            
    # display the reponse
    if len(result):
        st.header('AI Tech advancements in 2024')
        st.info(response)
        
 