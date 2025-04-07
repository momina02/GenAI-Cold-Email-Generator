import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv


load_dotenv()



class Chain:
    def __init__(self):
        self.llm = ChatGroq (groq_api_key = os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0)
        
    def extracted_text(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPE TEXT FROM WEBSITE:
            {page_data} 
            ### INSTRUCTION
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON object containing 
            following keys: 'role', 'experience', 'skills' and 'description'.
            Do not return a list. Only return a single JSON object.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]
    
    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Momina Ather, an AI Engineer. 
        
        Passionate about creating intelligent, data-driven solutions. With expertise in AI and Machine Learning, I develop predictive models and automation tools, ensuring seamless integration into web platforms.
        I enjoy solving complex problems and gaining insights from data to create innovative software. 
        Whether implementing AI-driven decisions or enhancing functionality and design, I focus on delivering efficiency and scalability in every project.
        
        Your job is to write a cold email to the client regarding the job mentioned above describing my capability of fulfilling their needs.
        
        Also add the most relevant ones from the following links to showcase my portfolio: {link_list}
        Remember you are Momina, an AI Engineer. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        
        """)
        
        chain_email = prompt_email | self.llm

        res = chain_email.invoke({'job_description': str(job), 'link_list' : links} )

        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))