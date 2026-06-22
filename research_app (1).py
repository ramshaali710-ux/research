
import streamlit as st
import requests
import time

st.set_page_config(
    page_title="ResearchBot",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 ResearchBot")
st.caption("AI Research Assistant for Medical Scientists")

with st.sidebar:
    st.header("About")
    st.info("Built by Ramsha — Biochemistry Graduate + AI Developer")
    st.success("Search any medical topic!")
    st.warning("Powered by PubMed database")
    
    st.header("Popular Topics")
    topics = ["Diabetes","Cancer","Blood pH",
              "Biochemistry","Hepatitis","Malaria"]
    for topic in topics:
        if st.button(topic):
            st.session_state.search = topic

st.header("Search Research Papers")

col1, col2 = st.columns([3,1])
with col1:
    search_topic = st.text_input(
        "Enter research topic:",
        placeholder="e.g. Type 2 Diabetes"
    )
with col2:
    num_results = st.selectbox("Results:", [5, 10, 15])

if st.button("Search PubMed"):
    if search_topic:
        with st.spinner("Searching PubMed..."):
            try:
                response = requests.get(
                    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                    f"?db=pubmed&term={search_topic}&retmax={num_results}&retmode=json",
                    timeout=10
                )
                data = response.json()
                ids = data["esearchresult"]["idlist"]
                count = data["esearchresult"]["count"]
                
                st.success(f"Found {count} papers on {search_topic}!")
                st.subheader(f"Top {len(ids)} Papers:")
                
                for i, paper_id in enumerate(ids, 1):
                    time.sleep(0.3)
                    try:
                        detail = requests.get(
                            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                            f"?db=pubmed&id={paper_id}&retmode=json",
                            timeout=10
                        )
                        paper = detail.json()["result"][paper_id]
                        
                        with st.expander(
                            f"Paper {i}: {paper['title'][:80]}..."
                        ):
                            st.write("Title:", paper["title"])
                            st.write("Journal:", paper["fulljournalname"])
                            st.write("Date:", paper["pubdate"])
                            if paper["authors"]:
                                st.write("Authors:", 
                                    paper["authors"][0]["name"] + " et al.")
                            st.markdown(
                                f"[Read Full Paper](https://pubmed.ncbi.nlm.nih.gov/{paper_id}/)"
                            )
                    except:
                        st.warning(f"Could not load Paper {i} details")
                        
            except Exception as e:
                st.error("Search failed. Check internet connection!")
    else:
        st.warning("Please enter a topic!")

st.divider()
st.caption("ResearchBot — Helping researchers find papers faster!")
