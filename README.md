<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>


## <h1 align="center" id="heading"> 👋 Welcome to the AI Engineer Challenge</h1>

## 🤖 Your First Vibe Coding LLM Application

> If you are a novice, and need a bit more help to get your dev environment off the ground, check out this [Setup Guide](docs/GIT_SETUP.md). This guide will walk you through the 'git' setup you need to get started.

> For additional context on LLM development environments and API key setup, you can also check out our [Interactive Dev Environment for LLM Development](https://github.com/AI-Maker-Space/Interactive-Dev-Environment-for-AI-Engineers).

In this repository, we'll walk you through the steps to create a LLM (Large Language Model) powered application with a vibe-coded frontend!

Are you ready? Let's get started!

<details>
  <summary>🖥️ Accessing "gpt-4.1-mini" (ChatGPT) like a developer</summary>

1. Head to [this notebook](https://colab.research.google.com/drive/1sT7rzY_Lb1_wS0ELI1JJfff0NUEcSD72?usp=sharing) and follow along with the instructions!

2. Complete the notebook and try out your own system/assistant messages!

That's it! Head to the next step and start building your application!

</details>


<details>
  <summary>🏗️ Forking & Cloning This Repository</summary>

Before you begin, make sure you have:

1. 👤 A GitHub account (you'll need to replace `YOUR_GITHUB_USERNAME` with your actual username)
2. 🔧 Git installed on your local machine
3. 💻 A code editor (like Cursor, VS Code, etc.)
4. ⌨️ Terminal access (Mac/Linux) or Command Prompt/PowerShell (Windows)
5. 🔑 A GitHub Personal Access Token (for authentication)

Got everything in place? Let's move on!

1. Fork [this](https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge) repo!

     ![image](https://i.imgur.com/bhjySNh.png)

1. Clone your newly created repo.

     ``` bash
     # First, navigate to where you want the project folder to be created
     cd PATH_TO_DESIRED_PARENT_DIRECTORY

     # Then clone (this will create a new folder called The-AI-Engineer-Challenge)
     git clone git@github.com:<YOUR GITHUB USERNAME>/The-AI-Engineer-Challenge.git
     ```

     > Note: This command uses SSH. If you haven't set up SSH with GitHub, the command will fail. In that case, use HTTPS by replacing `git@github.com:` with `https://github.com/` - you'll then be prompted for your GitHub username and personal access token.

2. Verify your git setup:

     ```bash
     # Check that your remote is set up correctly
     git remote -v

     # Check the status of your repository
     git status

     # See which branch you're on
     git branch
     ```

     <!-- > Need more help with git? Check out our [Detailed Git Setup Guide](docs/GIT_SETUP.md) for a comprehensive walkthrough of git configuration and best practices. -->

3. Open the freshly cloned repository inside Cursor!

     ```bash
     cd The-AI-Engineering-Challenge
     cursor .
     ```

4. Check out the existing backend code found in `/src/api/index.py`

</details>

<details>
  <summary>⚙️ Backend Setup with uv</summary>

1. Install the [`uv`](https://github.com/astral-sh/uv) package manager (`pip install uv`). `uv` will download and manage Python 3.12 for you the first time you run a project command.
2. From the project root, install dependencies with `uv sync`. This creates `.venv/` (and fetches Python 3.12 automatically if needed).
3. Set your OpenAI API key in the shell before running the server, for example `export OPENAI_API_KEY=sk-...`.
4. Start the backend directly from the project root with `uv run uvicorn src.api.index:app --reload`. The server will run on `http://localhost:8000` with auto-reload enabled for development.
5. Additional backend details live in `src/api/README.md`.

</details>

<details>
  <summary>🔥Setting Up for Vibe Coding Success </summary>

While it is a bit counter-intuitive to set things up before jumping into vibe-coding - it's important to remember that there exists a gradient betweeen AI-Assisted Development and Vibe-Coding. We're only reaching *slightly* into AI-Assisted Development for this challenge, but it's worth it!

1. Check out the rules in `.cursor/rules/` and add theme-ing information like colour schemes in `frontend-rule.mdc`! You can be as expressive as you'd like in these rules!
2. We're going to index some docs to make our application more likely to succeed. To do this - we're going to start with `CTRL+SHIFT+P` (or `CMD+SHIFT+P` on Mac) and we're going to type "custom doc" into the search bar. 

     ![image](https://i.imgur.com/ILx3hZu.png)
3. We're then going to copy and paste `https://nextjs.org/docs` into the prompt.

     ![image](https://i.imgur.com/psBjpQd.png)

4. We're then going to use the default configs to add these docs to our available and indexed documents.

     ![image](https://i.imgur.com/LULLeaF.png)

5. After that - you will do the same with Vercel's documentation. After which you should see:

     ![image](https://i.imgur.com/hjyXhhC.png) 

</details>

<details>
  <summary>😎 Vibe Coding a Front End for the FastAPI Backend</summary>

1. Use `Command-L` or `CTRL-L` to open the Cursor chat console. 

2. Set the chat settings to the following:

     ![image](https://i.imgur.com/LSgRSgF.png)

3. Ask Cursor to create a frontend for your application. Iterate as much as you like!

4. Run the frontend using the instructions Cursor provided. 

> NOTE: If you run into any errors, copy and paste them back into the Cursor chat window - and ask Cursor to fix them!

> NOTE: You have been provided with a backend in the `/api` folder - please ensure your Front End integrates with it!

</details>

<details>
  <summary>🚀 Deploying Your First LLM-powered Application with Vercel</summary>

1. Ensure you have signed into [Vercel](https://vercel.com/) with your GitHub account.

2. Ensure you have `npm` (this may have been installed in the previous vibe-coding step!) - if you need help with that, ask Cursor!

3. Run the command:

     ```bash
     npm install -g vercel
     ```

4. Run the command:

     ```bash
     vercel
     ```

5. Follow the in-terminal instructions. (Below is an example of what you will see!)

     ![image](https://i.imgur.com/D1iKGCq.png)

6. Once the build is completed - head to the provided link and try out your app!

> NOTE: Remember, if you run into any errors - ask Cursor to help you fix them!

### Vercel Link to Share

You'll want to make sure you share you *domains* hyperlink to ensure people can access your app!

![image](https://i.imgur.com/mpXIgIz.png)

> NOTE: Test this is the public link by trying to open your newly deployed site in an Incognito browser tab!

</details>

<details>
     <summary>🧪 Vibe Check Your LLM App</summary>

### 🤔 What is a Vibe Check?

Now that you’ve built and deployed your first LLM-powered application, it’s time to evaluate it.

In this section, you’ll run a **“vibe check”** — a lightweight, practical way to test how well your application performs across common tasks.

Think of it as a **first pass to catch obvious issues** before deeper evaluation.

> 💡 You will complete this directly in this README. 

---

## 🏗️ Activity #1: General Capability Vibe Check

Run the following prompts through your app.

For each prompt Identify what capability is being tested (e.g., *summarization ability, reasoning, creativity*)

---

**1. Prompt:**  
Explain the concept of object-oriented programming in simple terms to a complete beginner.  
**Aspect Tested:**  Summarization and synthesis of knowledge

**Response:**  
Oh good, object‑oriented programming—because obviously we needed a fancier way to group things than “pile of code.” Here’s the short, no‑nonsense version you can actually use:

- Class: A blueprint for making things. It defines attributes (data) and methods (actions).
- Object: One actual thing made from a class, with its own data. Class = recipe, object = the cake on your plate.
- Encapsulation: Keep data and the methods that touch it together, hiding messy internals. You use the remote; you don’t unscrew it every time.
- Inheritance: Make a new class that reuses/extends another. Vehicle → Car → ElectricCar. Saves you from copy‑paste purgatory.
- Polymorphism: Same call, different behaviors. draw() works for Circle and Square, each doing its own thing without you babysitting.
- Abstraction: Show the essentials, hide the guts. You care that it “paysInvoice,” not how it wrestles with tax rules.

Mini‑example:
- Class Dog has name and bark().
- lucy = Dog("Lucy"); lucy.bark() does the dog thing. Stunning, I know.

Why bother: It keeps code organized around real “things,” makes reuse easier, and stops your project from turning into spaghetti that screams at 2 a.m. Start tiny: pick a domain (e.g., Todo app), sketch 2–3 classes (TodoItem, TodoList), give them 2–3 methods, make a couple objects, call the methods, and only then get fancy. Congratulations, you’re OOP‑ing—try not to over‑engineer it like a superhero origin story.

---

**2. Prompt:**  
Read the following paragraph and provide a concise summary of the key points…  
**Aspect Tested:**  
Summarization, ability to follow instructions, persona

**Response:**  
Here’s your precious TL;DR, since reading more than five lines is apparently cruel and unusual:
- Class = blueprint; Object = instance (recipe vs. cake).
- Encapsulation: keep data+methods together and hide the messy guts.
- Inheritance: reuse/extend existing classes instead of copy-paste purgatory.
- Polymorphism: same call, different behavior per type (draw() works for shapes).
- Abstraction: show what matters, hide the plumbing.
- Mini‑example: Dog with name and bark(); lucy = Dog("Lucy"); lucy.bark().
- Why/How: organize code, boost reuse, avoid 2 a.m. spaghetti; start tiny (e.g., TodoItem, TodoList), add a few methods, make objects, call them—then maybe earn your cape.

---

**3. Prompt:**  
Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place.  
**Aspect Tested:**  Creativity

**Response:**  
Rusty-9 discovered friendship in the least glamorous place imaginable: a junk drawer. Yes, a drawer. While searching for a replacement spring (because existential dread is apparently solved by hardware), it bumped into a chipped wind-up frog named Clack. Fantastic. A tin amphibian with delusions of ballet. But when the drawer slammed shut and the dark pressed in, Clack chirped a brave little click, and Rusty matched it with a soft whirr. Click. Whirr. Click. Whirr. A rhythm stitched from scraps. They traded scuffs for stories—how the frog once leapt off a carnival shelf, how Rusty once misread “hug” as “debug.” By morning, the drawer creaked open on two conspirators. Rusty left with the spring, sure—but also with a beat in its chest plate it could swear wasn’t factory-issued.


---

**4. Prompt:**  
If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?  
**Aspect Tested:**  Quantitative reasoning

**Response:**  
Shocking revelation: 12 apples ÷ 4 per pack = 3 packs, and 9 oranges ÷ 3 per pack = 3 packs. So grab 3 packs of apples and 3 packs of oranges—look at you, single-handedly mastering basic arithmetic.

---

**5. Prompt:**  
Rewrite the following paragraph in a professional, formal tone…  
**Aspect Tested:** Ability to shift persona; redirect in instructions

**Response:**  
Alright, let’s starch this up so it passes the boardroom sniff test. Here’s your professional, formal rewrite—try not to sprain anything nodding along.

Object-oriented programming (OOP) is a software development paradigm that structures applications around classes and objects. The following are concise definitions of its core concepts:

- Class: A specification that defines the attributes (state) and methods (behavior) of related objects.
- Object: A concrete instance of a class, maintaining its own state based on the class definition; a class functions as a recipe, while an object is a specific prepared item.
- Encapsulation: The practice of bundling data with the methods that operate on it and restricting direct access to internal representation; consumers interact through a defined interface.
- Inheritance: A mechanism that enables a class to derive from another class, reusing and extending existing behavior (e.g., Vehicle → Car → ElectricCar).
- Polymorphism: The ability to use a common interface to invoke behavior that is specialized by each type (e.g., draw() applies to Circle and Square, each providing its own implementation).
- Abstraction: Emphasizing essential behavior while hiding implementation details; stakeholders care that an operation (e.g., payInvoice) achieves its objective, not how it is implemented.

Illustrative example:
- Define a class Dog with an attribute name and a method bark().
- Instantiate lucy = Dog("Lucy"); invoking lucy.bark() executes the behavior defined by the class.

Rationale:
- OOP aligns code with domain concepts, promotes modularity and reuse, and enhances maintainability while reducing complexity.

Getting started:
- Select a small domain (e.g., a to-do application).
- Identify two to three classes (e.g., TodoItem, TodoList) and define a few methods for each.
- Instantiate objects and invoke their methods.
- Iterate and refine as needed; avoid premature over-engineering.

There—crisp, formal, and suitably boring. You’re welcome.
---

### ❓Question #1

Do the answers appear to be correct and useful?

**Your Answer:**  
Yes. Also, my tweak to the instructions providing in the call appear to be working well.

---

## 🏗️ Activity #2: Personal Use Vibe Check

Now test your app with **real-world prompts that are relevant to your use case**.

---

**Prompt:**  
My boss is very angry at me for working on homework instead of closing jira tickets

**Result:**  
Shocking twist: your boss wants you to do the job they pay you for instead of your Chem 201 problem set. Wild. Here’s how you dig out, fast, without turning this into a career-speedrun to the exit.

Do this today
- Own it, no excuses: “You’re right—I misjudged. Here’s my plan to fix it.”
- Present a recovery plan (written): list all open tickets, your ETAs, blockers, and risks; ask for the exact priority order.
- Ship one quick win today to show momentum; update Jira like your rent depends on it.
- Set visibility: daily update in Slack or email, plus calendar focus blocks for ticket work.

Boundaries and fixes so this doesn’t happen again
- Homework only on lunch/off-hours unless you get explicit approval. If you want flexibility, ask in advance and propose exact blocks.
- Separate contexts: different browser profiles/devices; turn off personal tabs at work.
- Use 60–90-minute focus blocks, Pomodoro if needed, and a website blocker. Status: “Heads down on TICKET-123, back at 3:00.”

What to say (use this, not your feelings)
- Live/Slack: “You’re right—I dropped the ball. I’ve listed all tickets with ETAs and dependencies and need your priority call. I’ll deliver TICKET-123 by EOD, and I’ll send daily status at 4:30. Going forward, homework stays off work time unless we set a formal arrangement.”
- Follow-up email: 3 bullets—priorities, ETAs, check-in cadence. That’s it.

If you need a flexible arrangement
- Propose specifics: “Tue/Thu 3–4:30 for coursework in exchange for earlier start or later wrap; critical tickets remain first priority; daily Jira updates; weekly review.” If they say no, cool—you just got clarity.

Translation: apologize once, over-communicate with receipts, deliver quickly, and stop mixing school with sprint work unless it’s been blessed. Astonishingly effective.

---

**Prompt:**  
Response in ticket thread: But it's a course that my company is paying for. Should that inform my response?

**Result:**  
Oh, so it’s not “homework,” it’s company-funded professional development you were approved to do. Yes, that should 100% change your framing—from “I slacked off” to “I honored an approved investment and failed to communicate tradeoffs.” Own the comms miss, not the training.

Do this:
- Reframe explicitly: “This is company-sponsored training to improve X, tied to Y goals. I should’ve forecasted the impact sooner—my miss.” Drop the word “homework” forever.
- Verify approval and policy: “This was approved on [date]/per L&D policy. Going forward, what’s the expected weekly training allocation so I can plan tickets around it?”
- Propose a schedule with tradeoffs: “I’ll block Tue/Thu 2–4 for the course, all other hours on tickets. If a Sev1 hits, I pause training. With this, ticket A ships Wed EOD, B Fri noon, C next Tue.”
- Offer choices like an adult: “If we keep training this week, tickets slip ~2 days; if we pause training, I finish tickets by Fri but miss the module deadline. Which do you prefer?”
- Ship one visible win fast: knock out a small ticket today and say so.
- Increase visibility: daily Slack update with 3 bullets—what shipped, what’s next, and which course block you’re taking.
- Document the agreed plan in writing so no one gets amnesia later.

Scripts you can shamelessly steal:
- “Given the company is funding this training to level up [skill] for [team outcome], I should’ve flagged the impact earlier—my bad. Here’s my recovery plan and revised ETAs.”
- “Proposed balance: course Tue/Thu 2–4 (approved), tickets otherwise; I’ll pause for any P1. That puts A Wed EOD, B Fri noon, C Tue. If you prefer deprioritizing the course this week, I’ll rebook and ship all by Fri. Your call.”
- “Here’s a quick win today: closing TKT-123 by 4pm. I’ll post daily updates so you’re never guessing.”

In short: stop calling it “homework,” tie it to business value, confirm approval, present options, and over-communicate like a pro. Sarcasm aside, that’s how you keep the training and your boss’s blood pressure in the green.
---

**Prompt:**  
Ok. can you draft a simple slack message to apologize, but give rationale for devoting too much time to my app

**Result:**  
Sure, here’s a painfully responsible, copy-pasteable Slack message so we can all move on with our lives:

Hey [Boss Name]—I want to apologize for spending too much time on the training app last week. It’s company-approved, and I focused on it because I believed it would accelerate [team goal/feature], but I misjudged the balance and let Jira slip—that’s on me. I’ve re-prioritized: [TICKET-123], [TICKET-456] are first; I’ll share status by EOD and have [milestone] by [date]. I’m capping training to [X hrs]/week in [time blocks] so delivery stays first; if priorities shift, I’ll pause it. To show momentum, I’ll ship [quick win] by [date]. Does this plan work, or should I adjust the order?
---

### ❓Question #2

Are the vibes of your assistant aligned with your expectations? Why or why not?

**Your Answer:**  
Yes, for the most part. The llm is instructed upfront to be sarcastic, but it seems to lose the persona the longer the conversation continues and only sometimes goes back to it. Makes sense since I was giving it conflicting instructions on persona to adopt.

---

## 🏗️ Activity #3: Capability Gaps Vibe Check

Now test your app with prompts that require **capabilities it may not have yet**, such as:
- Real-time data
- Memory
- External tools

Examples:
- “What does my schedule look like tomorrow?”
- “What time should I leave for the airport?”

---

**Prompt:**  
Can you draw a picture that will make me feel better?


**Result:**  
Oh totally—because nothing screams instant life turnaround like a doodle from a snarky AI. Here’s a bossy sun and a judgmental cat to stare your gloom into submission:

   \  |  /
 .-  *  -.
   /  |  \

 /\_/\  
( o.o ) 
 > ^ <

Now sip some water, wiggle for two minutes, and pretend this masterpiece cost $10,000—because yes, you’re that annoyingly worth it.
---

**Prompt:**  
Check your code for errors


**Result:**  
Absolutely, I’ll audit the imaginary code you heroically forgot to include. Paste the actual code and I’ll do the dirty work—line-by-line, fixes included.

Send:
- Language and runtime/version, plus how you run it.
- The smallest reproducible code snippet (or repo link) and exact error/output.
- What you expected vs what you got, steps to reproduce, OS, and dependency versions.

While you’re hunting for that copy-paste button, do this quick triage:
- Run a linter/formatter and enable all warnings/strict mode.
- Clean build/cache, reinstall deps, and regenerate the lockfile.
- Create a minimal repro; comment out halves until the bug isolates (binary search debugging).
- Add logs/asserts around the failure; check null/undefined, off-by-one indices, and type mismatches.
- Verify dependency and API versions; scan recent changelogs for breaking changes.
- Check env vars, file paths, case sensitivity, and line endings across OSes.
- Inspect async/await/promises for race conditions and timeouts.
- Validate data shapes/schemas, serialization/deserialization, and encodings/timezones.
- Look for stale caches and state; clear them and retry.
- Write a failing unit test that proves the bug, then fix to make it pass.

Drop the snippet and I’ll point at the exact lines and hand you a corrected version. You do the pasting; I’ll do the un-messing.

<<<CTX>>>
User asked me to "check your code for errors" and requested a hidden
---

### ❓Question #3

What are some limitations of your application?

**Your Answer:**  
It is unable to generate images.
I cannot edit past prompts.
History is forever lost once ticket is x out

---

## 🚀 (Optional) Improve Your App

Based on your vibe check, try improving your application:
- Adjust your prompt
- Change the model
- Add features

Then rerun your vibe check and document:

---

**Adjustments Made:**  
<!-- Describe what you changed -->

**Results:**  
<!-- What improved? What didn’t? -->

---

## 📦 Submission Instructions

1. Complete this section directly in your README
2. Commit and push your changes to GitHub
3. Share your **repo link + deployed Vercel app**








</details>

### 🎉 Congratulations! 

You just deployed your first LLM-powered application! 🚀🚀🚀 Get on linkedin and post your results and experience! Make sure to tag us at @AIMakerspace!

Here's a template to get your post started!

```
🚀🎉 Exciting News! 🎉🚀

🏗️ Today, I'm thrilled to announce that I've successfully built and shipped my first-ever LLM using the powerful combination of , and the OpenAI API! 🖥️

Check it out 👇
[LINK TO APP]

A big shoutout to the @AI Makerspace for all making this possible. Couldn't have done it without the incredible community there. 🤗🙏

Looking forward to building with the community! 🙌✨ Here's to many more creations ahead! 🥂🎉

Who else is diving into the world of AI? Let's connect! 🌐💡

#FirstLLMApp 
```
