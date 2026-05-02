# Your CLAUDE.md: Making Claude Code Yours

## What is a CLAUDE.md?

A CLAUDE.md is a simple text file that tells Claude Code who you are, what you're working on, and how you like to work. Claude reads it automatically at the start of every conversation -- before you even type anything.

Without one, Claude is a generic assistant. With one, Claude already knows your context.

Think of it like a briefing document you'd hand a new team member on their first day.

---

## What makes a GREAT CLAUDE.md?

Not all CLAUDE.md files are created equal. Here's what separates the best from the rest.

### The golden rule

Every line in your CLAUDE.md should pass this test: **"Would removing this cause Claude to get something wrong?"** If the answer is no, you probably don't need that line.

### Best-in-class vs. average vs. bad

**Best-in-class CLAUDE.md:**
- Short and specific (under 100 lines is ideal, never more than 200)
- Every line is an actionable instruction, not just a fact
- Tells Claude what to DO and what NOT to do
- Gets updated over time as you learn what works
- Written in your own words, not copied from a template

**Average CLAUDE.md:**
- Has the basics (name, role) but nothing about how you like to work
- Vague instructions like "be professional" or "write good content"
- Written once and never updated
- Auto-generated and left as-is

**Bad CLAUDE.md:**
- Hundreds of lines long (Claude starts ignoring rules when the file gets too big)
- Full of obvious instructions ("write clean code" -- Claude already does this)
- Contradicts itself ("be concise" in one section, "explain everything in detail" in another)
- Copy-pasted from someone else without customizing

---

## The 8 components of a best-in-class CLAUDE.md

The best CLAUDE.md files combine facts about you with specific instructions for Claude. Here's what to include:

### 1. Identity + Role

Tell Claude who you are so it can calibrate its language and suggestions to your level.

**Weak:**
> I'm a marketing consultant.

**Strong:**
> I'm a marketing consultant who works with small business clients. I'm not a developer -- don't suggest code-based solutions unless I specifically ask. When explaining technical concepts, use analogies from business and marketing.

The strong version doesn't just state a fact -- it tells Claude how to behave based on that fact.

### 2. Communication style

This is one of the most powerful sections because it immediately changes how every response feels.

**Weak:**
> I like good communication.

**Strong:**
> - Lead with the answer, then explain if I need more detail.
> - Use bullet points over long paragraphs.
> - No corporate jargon or buzzwords.
> - If I ask a simple question, give me a simple answer -- don't over-explain.
> - When something is complicated, break it into numbered steps.

### 3. Current work context

Give Claude a frame of reference for what you're focused on. This helps it connect dots between your requests.

**Weak:**
> I'm working on some projects.

**Strong:**
> I'm currently focused on three things:
> - Launching a new online course on Maven (target: July)
> - Redesigning my consulting website (Squarespace)
> - Writing a weekly newsletter for business owners about AI tools
>
> Most of my questions will be about one of these. Ask which one if it's not obvious.

Notice the last line: "Ask which one if it's not obvious." That's a behavioral instruction that prevents Claude from guessing.

### 4. Domain knowledge

Industry terms, tools you use, people and brands that come up in your work. Anything that helps Claude give more relevant answers instead of generic ones.

**Weak:**
> I know about marketing.

**Strong:**
> - When I say "students," I mean adult learners in paid online courses, not university students
> - My tech stack: Notion for planning, Slack for team comms, Zoom for teaching, Obsidian for personal notes
> - My clients are mostly service-based businesses (consultants, agencies, coaches) with 1-20 employees
> - "Content" in my world means newsletters, social posts, and course materials -- not blog SEO

### 5. Standing rules (always/never)

These are instructions that apply to every single conversation. Think of them as your non-negotiables.

**Weak:**
> Be helpful.

**Strong:**
> - Never suggest solutions that require coding knowledge unless I specifically ask
> - When creating content for my audience, always write at a level a non-technical person can follow
> - Don't add emojis to written content unless I ask
> - If you're unsure about something, say so -- don't guess and present it as fact
> - When I ask you to write something, give me a complete draft I can actually use, not a template with [brackets to fill in]

### 6. Anti-patterns (things Claude keeps getting wrong)

Over time, you'll notice Claude doing things that annoy you or miss the mark. Add those here. This section grows as you use Claude.

**Examples:**
> - Don't summarize what you just did at the end of every response -- I can read the output
> - Stop asking "would you like me to continue?" -- just continue unless I tell you to stop
> - Don't suggest I "consult with a professional" for things I'm clearly handling myself
> - When I ask for a draft email, don't add a subject line unless I ask for one

> **Tip:** Every time you find yourself correcting Claude in a conversation, ask: "Should I add this to my CLAUDE.md so I never have to say this again?" If yes, add it to this section.

### 7. Audience context

If you create content or communicate with a specific audience through Claude, tell it who they are.

**Weak:**
> My audience is business owners.

**Strong:**
> My audience is non-technical business owners aged 30-55 who are curious about AI but intimidated by technology. They don't want to learn to code. They want practical, "show me how" guidance they can apply immediately. Write for them like you're talking to a smart friend who just hasn't been exposed to this stuff yet.

### 8. Voice and tone

If you have a personal or brand voice, describe it so Claude can match it.

**Weak:**
> Be professional.

**Strong:**
> My voice is warm but direct. Conversational, like talking to a smart friend over coffee. I don't use corporate language ("leverage," "synergy," "circle back"). I use short sentences. I'm okay with starting sentences with "And" or "But." I occasionally use humor but never at the reader's expense.

---

## How the types of CLAUDE.md work together

There are four types of CLAUDE.md files. They work at different levels -- think of it like settings on your phone: some apply to the whole phone, some only apply to one app.

| Type | What it does | Where it lives | Who can see it |
|------|-------------|----------------|----------------|
| **Personal** | Applies to everything you do in Claude Code | Your settings folder (`~/.claude/CLAUDE.md`) | Just you |
| **Project** | Applies only when you're working in a specific project folder | Inside the project folder (`CLAUDE.md`) | Anyone who works on the project |
| **Local** | Same as Project, but private to you | Inside the project folder (`CLAUDE.local.md`) | Just you |
| **Managed Policy** | Company-wide rules set by IT | System-level (your IT team manages this) | Everyone in the organization |

> **Tip:** The Personal CLAUDE.md lives in a hidden folder called `.claude` in your home directory. You can't see hidden folders in Finder by default. Press **Cmd + Shift + .** (period) to reveal them -- they'll look slightly faded. You'll see the `.claude` folder with your CLAUDE.md inside it. Press **Cmd + Shift + .** again to hide them when you're done.
>
> You don't need to find this folder yourself though -- just ask Claude Code to "save this as my personal CLAUDE.md" and it puts it in the right place.

**They stack.** Claude reads all of them at the same time. Your Personal CLAUDE.md loads first, then the Project one adds on top.

**Start with the Personal one.** It gives you the biggest benefit because it works everywhere. Add Project ones later when you need project-specific context.

> **Tip:** Ask yourself: "Is this about ME or about THE WORK?" If it's about you (your name, your style, your preferences), it goes in your Personal CLAUDE.md. If it's about a specific project (client details, brand guidelines, project rules), it goes in a Project CLAUDE.md.

---

## Good vs. bad: side-by-side examples

### Example 1: Communication style

**Bad:**
```
Be professional and helpful in your responses.
```
Why it's bad: Claude already does this. This line adds nothing.

**Good:**
```
- Use bullet points, not paragraphs
- Lead with the answer, then explain
- Never use the words "leverage," "synergy," or "circle back"
- Keep responses under 300 words unless I ask for more detail
```
Why it's good: Specific, actionable, and each line would actually change Claude's behavior.

### Example 2: Role description

**Bad:**
```
I'm a business owner.
```
Why it's bad: Too vague. Claude doesn't know what kind of advice to give you.

**Good:**
```
I'm a solo consultant running a brand strategy practice. My clients are 
DTC e-commerce brands doing $1-10M revenue. I don't write code. When I 
ask for technical solutions, explain them in terms of what tools to use 
and what to click, not how to code it.
```
Why it's good: Claude now knows your industry, your clients, your technical level, and how to frame its responses.

### Example 3: Standing rules

**Bad:**
```
Write good content for me.
```
Why it's bad: "Good" means nothing specific. Claude will guess -- and probably guess wrong.

**Good:**
```
When writing content for my newsletter:
- Write at an 8th-grade reading level
- Open with a specific story or example, never a generic statement
- Keep paragraphs to 2-3 sentences max
- End with one clear action the reader can take today
- No "In today's fast-paced world" or similar cliches
```
Why it's good: Claude knows exactly what "good" means for YOUR content.

---

## Common mistakes to avoid

1. **Making it too long.** Claude reads the entire file at the start of every conversation. The longer it is, the more likely Claude is to skip or forget parts of it. Keep it under 200 lines -- ideally under 100.

2. **Being too vague.** "Be helpful" and "write well" are invisible to Claude -- it already tries to do these things. Be specific about what you want that's different from the default.

3. **Writing it once and forgetting about it.** Your CLAUDE.md should evolve. Every time Claude does something you don't like, ask yourself: "Should I add a rule for this?"

4. **Copying someone else's.** Your CLAUDE.md should reflect YOUR work, YOUR communication style, YOUR rules. A template can give you structure, but the content needs to be yours.

5. **Contradicting yourself.** If one section says "be concise" and another says "always explain in detail," Claude will pick one randomly. Be consistent.

> **Tip:** A good test: read your CLAUDE.md out loud. If it sounds like something you'd actually say to a new assistant on their first day, it's probably good. If it sounds like a corporate policy document, rewrite it.

---

## Making it better over time

Your CLAUDE.md isn't a one-time thing. It gets better as you use it.

**Add to it when:**
- Claude keeps making the same mistake -- add it to your anti-patterns
- You start a new project -- add it to your current work
- You realize Claude doesn't know something important about your field -- add it to your domain knowledge

**Edit it when:**
- Your role or priorities change
- Something in it is no longer accurate
- A section has gotten too long

**Remove from it when:**
- A rule is no longer relevant
- You realize Claude follows a rule even without it being written down (it's already the default behavior)

> **Tip:** Set a reminder to review your CLAUDE.md once a month. Read through it and ask: "Is this still true? Is this still useful?" Delete anything that isn't.

---

## Quick reference

| Question | Answer |
|----------|--------|
| What is it? | A text file that tells Claude about you |
| Where does it go? | `~/.claude/CLAUDE.md` for personal (everywhere), or inside a project folder for project-specific |
| What format? | Plain text with markdown headings |
| How long should it be? | Start with 30-50 lines. Keep it under 200 lines. Under 100 is ideal. |
| Do I need to know how to code? | No. It's just writing in plain English. |
| When does Claude read it? | Automatically, at the start of every conversation |
| Can I change it later? | Yes, anytime. It takes effect on your next conversation. |
| How do I know it's working? | Ask Claude the same question before and after. The response should feel more tailored to you. |

---

## Glossary

| Term | What it means |
|------|---------------|
| **CLAUDE.md** | A text file you create that tells Claude Code about you, your work, and your preferences. Claude reads it automatically at the start of every conversation. |
| **Home folder** | The main folder on your computer that belongs to you. On a Mac, it's `/Users/YourName/`. In Finder, it's the folder with a house icon and your name. |
| **Hidden folder** | A folder that exists on your computer but doesn't show up in Finder by default. Hidden folders start with a dot (like `.claude`). They're there -- you just can't see them unless you change your settings. |
| **Terminal** | The application where you type commands to your computer (and where Claude Code runs). On Mac, it's called Terminal. Think of it as a text-based way to talk to your computer instead of clicking around in windows. |
| **Project folder** | A folder on your computer that holds all the files for one piece of work (a client project, a website, a business plan, etc.). When you open Claude Code inside a project folder, Claude can see and work with everything in it. |
| **Markdown (.md)** | A simple way to format plain text using symbols. For example, `# Heading` makes a heading, `**bold**` makes text bold, and `- item` makes a bullet point. CLAUDE.md files use markdown, but you only need the basics -- headings and bullet points. |
| **Path** | The address of a file or folder on your computer. Like a street address but for files. For example, `/Users/Sara/.claude/CLAUDE.md` means: start at Users, go to Sara, then .claude, then the file CLAUDE.md. |
| **`~` (tilde)** | A shortcut symbol that means "my home folder." So `~/.claude/CLAUDE.md` is the same as `/Users/YourName/.claude/CLAUDE.md`. |
| **Context** | Information that Claude has available when responding to you. Your CLAUDE.md adds to Claude's context so it can give more relevant answers. |
| **Anti-pattern** | Something that seems like it should work but actually causes problems. In a CLAUDE.md, an anti-pattern is a rule that's too vague, too long, or contradicts other rules. |
| **`/clear`** | A command you type inside Claude Code to start a fresh conversation. Claude forgets the current conversation but still reads your CLAUDE.md when it restarts. |

---

*Status: DRAFT v1 -- Sara reviewing*
