import streamlit as st
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

# Load secrets
neo4j_uri = st.secrets["NEO4J_URI"]
neo4j_user = st.secrets["NEO4J_USERNAME"]
neo4j_password = st.secrets["NEO4J_PASSWORD"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("Football Memories AI")

# Initialize connections and models
@st.cache_resource(show_spinner=False)
def init_resources(api_key):
   graph = Neo4jGraph(
       url=neo4j_uri,
       username=neo4j_user,
       password=neo4j_password,
       enhanced_schema=True,
   )
   graph.refresh_schema()
   chain = GraphCypherQAChain.from_llm(
       ChatOpenAI(api_key=api_key, model="gpt-4o"),
       graph=graph,
       verbose=True,
       show_intermediate_steps=True,
       allow_dangerous_requests=True,
   )
   return graph, chain

# Initialize resources only if API key is provided
if openai_api_key:
   with st.spinner("Initializing resources..."):
       graph, chain = init_resources(openai_api_key)
       st.success("Resources initialized successfully!", icon="🚀")

# Initialize message history
if "messages" not in st.session_state:
   st.session_state.messages = [
       {
           "role": "assistant",
           "content": "Hello! Ask me anything about International Football from 1872 to (the almost) present day!",
       }
   ]

# Muestra historial de mensajes en el chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def query_graph(query):
   try:
       result = chain.invoke({"query": query})["result"]
       return result
   except Exception as e:
       st.error(f"An error occurred: {str(e)}")
       return "I'm sorry, I encountered an error while processing your request."

# Reacción al prompt
if prompt := st.chat_input("Ask me anything about International Football..."):
    # Añade el mensaje del usuario al historial del chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Muestra mensaje del usuario en el contenedor del chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer if API key is provided
    if openai_api_key:
        with st.spinner("Thinking..."):
            response = query_graph(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.error("Please enter your OpenAI API key in the sidebar to use the chatbot.")