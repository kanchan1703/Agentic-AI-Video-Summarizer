# Agentic AI Video Summarizer Project
<br/>

The project is a web application built using **Streamlit** which allows users to upload  videos and analyze their content by asking specific questions related to it and also translate into various other languages. 
<br/>

The **phi library** is used to create the AI Agent, where I imported the **Google Gemini** model for the video analysis, and **DuckDuckGo Search**, a tool for web search, so that the agent can gather 
additional information.
<br/>

I also imported **google.generativeai** library, where I used Google services like **upload_file**, to upload the files for processing, and **get_file** to retrieve the processed file's results.
<br/>

For the translation of the analysis, I imported the **deep_translator** library from **GoogleTranslator**, which helps in translating the video analysis into different languages.

Also, I used **dotenv**, which helped me to load sensitive information like the **API key** from the **.env** file.
<br/>

And, used the inbuilt libraries like **time**, which helps in introducing delays(time for video processing to complete), **pathlib**, which helps in managing file paths and deleting the
 temporary files, **tempfile**, to create temporary files and store the uploaded videos.

