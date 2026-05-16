# PROJECT TRACKER
## Project 1: Career Digital Twin
**Week:** 1
**Framework:** Google ADK
**Date completed:** 2025-05-16
**Repo link:** https://github.com/gsegelov/career-digital-twin
**Status:** [x] Ed's baseline complete  [x] Extended  [ ] Portfolio-ready

---

## 1. WHAT I BUILT

### Ed's Baseline
A single AI agent loaded with the candidate's professional background that
answers recruiter questions in the candidate's voice using function calling.
The baseline demonstrates agent construction, system prompt engineering,
and context injection.

### My Version
Built the full baseline agent plus a job-matching tool (analyze_job_fit)
that accepts a job description, sends it alongside my resume to Gemini,
and returns a structured analysis: fit score (0-100), aligned skills,
skill gaps, and suggested positioning framing. The agent decides
autonomously when to call the tool based on user input.

### Architecture Flow
```
User message
     ↓
ADK Runner receives message, passes to agent
     ↓
Agent reads message + system prompt
     ↓
If job description detected → calls analyze_job_fit(job_description)
     ↓
Tool loads resume.md from disk
Tool sends resume + JD to Gemini with structured JSON prompt
Tool returns: {fit_score, aligned_skills, gap_skills, suggested_framing}
     ↓
Agent narrates the analysis in Gila's voice
     ↓
Response printed to terminal
```

---

## 2. SKILLS DEMONSTRATED

**Agentic Patterns:**
- [x] Agent construction and system prompt design — defined identity,
      knowledge, tone, and guardrails in SYSTEM_PROMPT
- [x] Tool / function calling — agent autonomously decides to call
      analyze_job_fit when it detects a job description
- [x] Stateful agents (memory) — InMemorySessionService maintains
      conversation history within a session

**Frameworks:**
- [x] Google ADK — Agent, FunctionTool, Runner, InMemorySessionService

**Engineering:**
- [x] External API integration — Gemini API via google-genai SDK
- [x] Structured output / output engineering — prompt engineering to
      force JSON output; markdown fence stripping for reliability
- [x] Async Python — async def main(), await, asyncio.run()
- [x] Environment management — .env with load_dotenv(), .gitignore

---

## 3. TECHNICAL DECISIONS

| Decision | Options Considered | What I Chose | Why |
|---|---|---|---|
| LLM provider | OpenAI / Gemini | Gemini 2.5 Flash | Cost-efficient for dev; swap to Pro for demos |
| Framework | OpenAI Agents SDK / Google ADK | Google ADK | Native Gemini support; GCP portfolio differentiator |
| Resume storage | Hardcoded string / external file | resume.md file | Easier to update; separates data from logic |
| JSON parsing | Direct parse / cleaned parse | Strip markdown fences first | Gemini sometimes wraps JSON in code fences |

---

## 4. WHAT I LEARNED

### Concepts I Now Understand Deeply
1. The difference between a function and an agent — a function does
   exactly what you tell it when you tell it; an agent decides when
   to call tools based on context
2. Why context injection matters — Gemini has no memory between API
   calls; you must include all relevant background in every prompt
3. How tool calling works — the agent reads the docstring to decide
   when to invoke a tool; the docstring is functional, not just docs
4. Why async/await is required — agentic frameworks wait on API calls
   constantly; async prevents the program from freezing during waits

### What Surprised Me
1. Gemini doesn't always follow formatting instructions — even when I
   explicitly said "return only JSON," it sometimes wrapped the response
   in markdown code fences, which broke the parser silently. I learned
   that production AI systems need defensive parsing, not just good prompts.
2. The hardest bugs weren't logic errors — they were invisible things
   like wrong import names and indentation escaping the function body.
   Reading error traces carefully was the actual skill.

### What I'd Do Differently
1. Start with google-genai instead of google.generativeai — would have
   avoided the deprecation warning and the Client() import confusion
2. Test the tool in isolation before wiring it to the agent — would
   have caught the JSON parsing issue faster

---

## 5. GEMINI-SPECIFIC NOTES

**Model used:** [x] gemini-2.5-flash (dev) / gemini-2.5-pro (demos)

**Integration method:** [x] google-genai direct API (tools.py)
                        [x] Google ADK (agent.py, main.py)

**Behavioral differences noticed:**
- Gemini sometimes wraps JSON responses in markdown code fences
  (```json ... ```) even when explicitly told not to — requires
  stripping before json.loads()
- Gemini is verbose by default; system prompt needs explicit
  conciseness instruction for tighter responses

**Prompt adjustments needed for Gemini:**
- Added markdown fence stripping to handle JSON wrapping behavior
- May need "respond concisely in 3-4 sentences" added to SYSTEM_PROMPT

**Compatibility issues / workarounds:**
- google.generativeai is deprecated — use google-genai (from google import genai)
- Both GOOGLE_API_KEY and GEMINI_API_KEY in .env causes a warning —
  keep only GOOGLE_API_KEY

---

## 6. BUSINESS PROBLEM SOLVED

**What problem does this solve in the real world?**
Job seekers spend significant time answering the same recruiter questions
repeatedly across multiple screening calls. This agent acts as an always-
available professional representative that can answer background questions
accurately and analyze job fit instantly — giving candidates a consistent,
well-framed response every time.

**Why does it matter / what's the business value?**
For a candidate in active job search, this reduces prep time per recruiter
call and ensures consistent, strategic positioning. For a recruiting firm,
the same pattern could screen candidates against job descriptions at scale —
replacing hours of manual resume review with structured, scored output.

**What company or team would use this?**
A talent acquisition team at Accenture or Deloitte could deploy this pattern
to pre-screen candidates against specific role requirements. A staffing firm
could use it to match candidates to open roles automatically. The underlying
pattern — structured analysis of a candidate against a JD — is used in
enterprise ATS systems costing thousands of dollars per seat.

---

## 7. PORTFOLIO PACKAGING

### GitHub README Summary
*(To be written during portfolio packaging weekend after Week 6)*

### What Makes It Portfolio-Grade
1. Job-matching tool returns structured JSON — not a prose response,
   a structured data object with score, lists, and framing. Shows
   output engineering thinking.
2. Built on Google ADK — a genuine differentiator from the 90% of
   candidates using OpenAI. Demonstrates GCP stack fluency.
3. Guardrails in system prompt — "never make up experience" constraint
   shows awareness of hallucination risk in production AI systems.

---

## 8. INTERVIEW DESCRIPTION

### 30-Second Version
In Week 1 of my AI engineering course, I built a Career Digital Twin —
an AI agent that represents my professional background and answers
recruiter questions in my voice. I extended it beyond the baseline with
a job-matching tool: you paste in a job description and the agent scores
my fit, identifies aligned skills, flags gaps, and suggests how to
position my experience for that specific role. The business use case is
talent matching — the same pattern enterprise ATS systems charge thousands
per seat for.

### 2-Minute Version
In Week 1 I built a Career Digital Twin using Google ADK and Gemini.
The agent is loaded with my professional background and answers recruiter
questions in my voice — but the interesting part is the job-matching tool
I added on top. When you paste in a job description, the agent calls the
tool autonomously, sends my resume and the JD to Gemini with a structured
prompt, and gets back a scored analysis — fit score, aligned skills, gaps,
and suggested framing — as a JSON object it then narrates.

The technical challenge I solved was getting reliable structured output
from Gemini. Even when you tell it to return only JSON, it sometimes wraps
the response in markdown fences, which breaks the parser. I added defensive
stripping logic to handle that — which is the kind of thing you only learn
by actually running the system and seeing it fail.

I chose Google ADK over OpenAI Agents SDK deliberately because I wanted
native Gemini integration and a GCP differentiator for the Dallas market.
If I were productionizing this, the next step would be a Streamlit interface
so it's browser-accessible, and a RAG layer so it can handle more complex
background documents without hitting context limits.

### Technical Follow-Up Answers

**Q: How does the job-matching tool work?**
A: It's a Python function registered as an ADK FunctionTool. When the
agent detects a job description in the user's message, it calls the
function autonomously. The function loads my resume from disk, injects
both the resume and the JD into a Gemini prompt that asks for structured
JSON output — fit score, aligned skills, gaps, and positioning advice —
then parses and returns that dictionary to the agent, which narrates it.

**Q: Why did you use Google ADK instead of OpenAI Agents SDK?**
A: Two reasons. First, ADK has native Gemini support — no LiteLLM
routing or compatibility workarounds. Second, GCP is a differentiator
in the DFW market; employers running Google Cloud stacks see ADK
fluency as directly relevant. The concepts map 1:1 to OpenAI Agents
SDK, so I got both.

**Q: How would you scale this for enterprise use?**
A: A few changes. First, replace the terminal interface with a Streamlit
or FastAPI layer so it's accessible via browser. Second, add a vector
database for the resume so it can handle longer, more complex backgrounds
via RAG. Third, add evaluation logging — track which tool calls produced
high-quality outputs so you can tune the prompts over time. The core
agentic pattern stays identical.

---

## 9. SKILLS GAP NOTES

- [ ] Async Python — understand the basics but need more exposure to
      complex async patterns (will appear in every subsequent project)
- [ ] ADK session management — InMemorySessionService works for demo;
      need to understand persistent session options for production

---

## 10. CONNECTIONS TO OTHER PROJECTS

- Tool calling pattern from this project appears in every subsequent project
- Context injection (resume → prompt) is the simplified version of RAG
  that appears in Week 3 Deep Research Agent
- Structured JSON output pattern reappears in Investment Analyst (Week 3)
- System prompt guardrail thinking applies to every agent going forward