import gradio as gr
import pandas as pd
from datetime import datetime

# Your greet function
def greet(research_topics="", relevance_criteria="", domain_filter=[], start_date=datetime(2024,9,5), hindex_threshold=0):
    papers_df = pd.DataFrame()  # Your actual papers DataFrame
    filtered_papers = papers_df.copy()

    # Apply your filters
    if hindex_threshold > 0:
        filtered_papers = filtered_papers[filtered_papers["max_author_hindex"] >= hindex_threshold]
    if len(domain_filter) > 0:
        filtered_papers = filtered_papers[
            filtered_papers["categories"].apply(lambda x: any([d in x for d in domain_filter]))
        ]
    if isinstance(start_date, datetime):
        filtered_papers = filtered_papers[
            filtered_papers["published"].dt.date >= start_date.date()
        ]
    # Continue filtering and processing as per your code

    summary = f"Found {len(filtered_papers)} papers"
    return summary, filtered_papers[["title", "abstract"]]

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("ArXiv Paper Finder")
    research_topics = gr.Textbox(label="Research Topics")
    relevance_criteria = gr.Textbox(label="Relevance Criteria")
    hindex_threshold = gr.Slider(0, 100, label="H-index Threshold")
    start_date = gr.Date(value="2024-09-05", label="Start Date")
    domain_filter = gr.CheckboxGroup(["cs.AI", "cs.ML"], label="Domains")

    summary = gr.Markdown()
    papers = gr.Dataframe()

    # Run button
    run_btn = gr.Button("Run")
    run_btn.click(greet, [research_topics, relevance_criteria, domain_filter, start_date, hindex_threshold], [summary, papers])

# Launch the app
demo.launch()
