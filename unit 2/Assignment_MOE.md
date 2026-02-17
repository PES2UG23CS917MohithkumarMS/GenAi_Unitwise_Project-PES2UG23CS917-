# Unit 2 Assignment: Building a Mixture of Experts (MoE) Router

**Topic:** Advanced Architecture using Groq API  
**Estimated Time:** 45-60 Minutes  
**Tools:** Python, Groq API, Dotenv

---

## 🎯 Objective
Your task is to build a **"Smart Customer Support Router"** using a Mixture of Experts (MoE) architecture.

In a real-world company, you don't want a "Generalist" AI handling everything. You want:
1.  A **Technical Expert** for bug reports.
2.  A **Billing Expert** for refund requests.
3.  A **Sales Expert** for new inquiries.

You will build a **Router** that takes a user query, decides which expert is best suited for it, and then forwards the query to that specific expert configuration.

---

## 🛠️ Requirements

### 1. Setup
- Install `groq` and `python-dotenv`.
- Set up your Groq API Key (variable: `GROQ_API_KEY`).

### 2. Define Your Experts
Create a configuration dictionary `MODEL_CONFIG` where you define your experts. 
*Note: Since we are using the Groq API, we can simulate different "experts" by using different **System Prompts** while using the same base model (e.g., `mixtral-8x7b-32768`).*

- **Technical Expert:** System prompt should be rigorous, code-focused, and precise.
- **Billing Expert:** System prompt should be empathetic, financial-focused, and policy-driven.
- **General Expert:** A fallback for casual chat.

### 3. The Router (The Core Task)
Write a function `route_prompt(user_input)` that uses an LLM call to classify the intent.
- Input: User's query string.
- Output: The **Category Name** (e.g., "technical", "billing", "general").
- **Constraint:** The router must return *only* the category name, nothing else.

### 4. The Orchestrator
Write a main function `process_request(user_input)` that:
1.  Calls `route_prompt` to decide the category.
2.  Selects the correct **System Prompt** based on the category.
3.  Calls the generic LLM (Mixtral) with that specific System Prompt + User Input.
4.  Returns the final answer.

---

## 📝 Example Output

**Input:**
> "My python script is throwing an IndexError on line 5."

**Logic:**
1.  **Router** sees "Python", "IndexError" -> Classifies as **"technical"**.
2.  **Orchestrator** loads the "Technical Expert" system prompt.
3.  **Expert** responds with a code fix.

**Input:**
> "I was charged twice for my subscription this month."

**Logic:**
1.  **Router** sees "charged", "subscription" -> Classifies as **"billing"**.
2.  **Orchestrator** loads the "Billing Expert" system prompt.
3.  **Expert** responds with refund policy info.

---

## 💡 Hints
- Use `temperature=0` for the Router (you want consistency).
- Use `temperature=0.7` for the Experts (you want creativity/flexibility).
- Your routing prompt should be very clear: *"Classify this text into one of these categories: [technical, billing, general]. Return ONLY the word."*

---

## 🚀 Bonus Challenge
Can you add a **"Tool Use"** expert? 
If the user asks for "current price of Bitcoin", route it to a function that (mock) fetches data, instead of just an LLM response.
