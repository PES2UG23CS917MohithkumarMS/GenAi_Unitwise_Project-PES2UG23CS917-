# Unit 2: Generative AI Concepts & LangChain

Welcome to the hands-on materials for Unit 2. This unit covers the foundations of building LLM applications using LangChain, Prompt Engineering, and RAG.

## 📂 Notebooks

### 1. [LangChain Foundation](./1_LangChain_Foundation.ipynb)
-   **Why LangChain?** Conceptual introduction.
-   **Setup:** Installing libraries and managing API keys securely.
-   **Models:** Temperature settings (Creativity vs. Consistency).
-   **Prompts & Parsers:** Using Templates and LCEL (LangChain Expression Language).

### 2. [Prompt Engineering Basics](./2_Prompt_Engineering.ipynb)
-   **Structure:** Role prompting (System/User/AI).
-   **Few-Shot Learning:** Teaching by example.
-   **Advanced Templates:** Partial formatting and reusable components.

### 3. [Advanced Prompting](./3_Advanced_Prompting.ipynb)
-   **Chain of Thought (CoT):** Step-by-step reasoning.
-   **Tree of Thoughts (ToT):** Exploratory reasoning (Branching & Judging).
-   **Graph of Thoughts (GoT):** Networked reasoning (Aggregation & Refinement).
-   *Note: This notebook uses the Groq API (Llama 3) for speed and logic demonstrations.*

### 4. [RAG & Vector Stores](./4_RAG_and_Vector_Stores.ipynb)
-   **Embeddings:** Understanding vector space (with Hugging Face models).
-   **Vector Stores:** Using FAISS for semantic search.
-   **RAG Pipeline:** Building a "Chat with your Data" system.
-   **Indexing Algorithms:** Deep dive into how vector databases scale (HNSW, PQ, IVF).

---

## 📝 Assignments

-   **[Assignment: Mixture of Experts (MoE)](./Assignment_MOE.md):** Build a Smart Routing system using Groq that directs queries to specialized Expert prompts.

## 🛠️ Setup
1.  Ensure you have a `.env` file with your API keys:
    ```bash
    GOOGLE_API_KEY=your_key_here
    GROQ_API_KEY=your_key_here
    ```
2.  Install dependencies (run the first cell in each notebook).
