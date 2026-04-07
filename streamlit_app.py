import streamlit as st
import requests
import time

API_URL = "https://autoagent-131706466702.us-west1.run.app"

st.set_page_config(
    page_title="AutoAgent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AutoAgent")
st.caption("A Multi-Agent LLM Orchestration System — Planner → Executor → Reviewer")
st.divider()

# Input
query = st.text_area(
    "Enter your technical query:",
    placeholder="e.g. Our startup expects 500K daily users. Should we use microservices or monolithic architecture?",
    height=100
)

col1, col2 = st.columns([1, 5])
with col1:
    run = st.button("🚀 Run Pipeline", type="primary", use_container_width=True)

if run and query.strip():
    with st.spinner("Running multi-agent pipeline..."):
        start = time.time()
        try:
            res = requests.post(
                f"{API_URL}/query",
                json={"query": query},
                timeout=120
            )
            elapsed = time.time() - start

            if res.status_code == 200:
                data = res.json()

                st.success(f"✅ Pipeline completed in {data.get('duration_seconds', round(elapsed, 1))}s")
                st.divider()

                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Subtasks", data.get("subtasks_count", "-"))
                m2.metric("Quality Score", f"{data.get('quality_score', 0):.2f}")
                m3.metric("Passed", "✅ Yes" if data.get("passed") else "❌ No")
                m4.metric("Duration", f"{data.get('duration_seconds', '-')}s")

                st.divider()

                # Final Answer
                st.subheader("📋 Final Answer")
                st.info(data.get("final_answer", "No answer returned."))

                # Gaps
                gaps = data.get("gaps", [])
                if gaps:
                    st.subheader("🔍 Identified Gaps")
                    for g in gaps:
                        st.warning(f"• {g}")

                # Task ID
                st.caption(f"Task ID: `{data.get('task_id', '-')}`")

            else:
                st.error(f"API error: {res.status_code} — {res.text}")

        except requests.exceptions.Timeout:
            st.error("Request timed out. The pipeline is taking longer than expected. Please try again.")
        except Exception as e:
            st.error(f"Error: {e}")

elif run and not query.strip():
    st.warning("Please enter a query first.")

    