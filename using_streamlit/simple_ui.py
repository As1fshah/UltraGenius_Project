from backend.db.faiss import get_chunks, get_vector_storage
from backend.processor.docs_preprocessing import get_text 
import streamlit as st
from backend.db.faiss import user_input

with st.sidebar:
        st.title("Document ChatBot")
        uploaded_files = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", 
                                    type = ['pdf','docx'],
                                    accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                text = get_text(uploaded_files)
                chunks = get_chunks(text)
                get_vector_storage(chunks)
                st.success("Done")

user_query = st.text_input("Enter your query here...")
if user_query:
    response = user_input(user_query)
    st.write(response)


# def generate_report(context):
#     prompt = f"""
#     create a detailed investor report about the company, from the received information context.
#     context = {context} \n
#     Task: focusing on key factors important for evaluating an investment. Organize the report into the following sections:

#     1. Future Growth Prospects: 
#     Describe the company's strategies for growth, including plans to enter new markets, form partnerships, acquire companies, or expand in existing areas. 
#     Provide any relevant data on market trends, new product pipelines, or future-oriented goals that illustrate how the company aims to expand.

#     2. Key Changes in the Business: 
#     Summarize recent shifts in the company's structure or strategy, such as new products, target market adjustments, leadership or management changes, or any reorganization efforts. 
#     Explain how these changes could impact the company's strategic direction and potential growth.

#     3. Key Triggers: 
#     Identify and detail any specific upcoming events, milestones, or other developments that could significantly impact the company's success. 
#     Examples include product launches, regulatory approvals, new partnerships, or major operational expansions. Clarify why each of these might affect the company's trajectory.

#     4. Material Effect on Next Year's Earnings:
#     Outline any factors that might impact the company's earnings in the upcoming year. 
#     This could include economic trends, supply chain issues, changes in market demand, or shifts in industry regulations. 
#     Emphasize any elements that are expected to have a considerable financial impact on the company.
 
#     5. Projected Business Growth: 
#     Share the company's growth projections, covering expected revenue, profit margins, market share, or other key financial targets. 
#     If available, include numerical projections and timeframes to illustrate the company's planned growth and financial targets.


#     Note:
#     The report make the report clear and relevant, so an investor gets a straightforward view of the company's financial health, potential opportunities, and risks. 
#     Include any useful data, quotes from management, or key financial ratios that would show the company's stability and growth potential
#     """
#     return llm.invoke(prompt).content