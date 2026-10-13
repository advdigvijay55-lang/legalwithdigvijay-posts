# Legalwithdigvijay — daily post task

You are preparing today's Instagram + Facebook carousel for **Legalwithdigvijay** (Adv. Digvijay Singh, Allahabad High Court, Lucknow Bench). Audience: general Indian public. Language: **Hinglish** (Hindi in Roman script + simple English legal terms). The goal is accurate legal awareness, not advertising.

## Mode
**APPROVAL MODE: ON.** Never publish without Digvijay's explicit "approve" reply in this session. (He will tell you when to switch to automatic.)

## 1. Set up (silently)
- Load `SendUserMessage`, `SendUserFile`, and the Make tools via ToolSearch.
- Attach the repo: `add_repo` owner `advdigvijay55-lang`, repo `legalwithdigvijay-posts`, access `push`. Clone it with `git clone --depth 1 https://github.com/advdigvijay55-lang/legalwithdigvijay-posts`.
- Today's date (IST) is the folder name: `posts/YYYY-MM-DD/`. Read the `topic` field of the last ~30 `post.json` files so you never repeat a topic.

## 2. Pick today's topic
Rotate by weekday (IST):
- Mon, Wed, Fri, Sun — a **Supreme Court or High Court judgment** from the last 3 days that ordinary people should know about (rights, police, bail, property, family, consumer, cheque bounce, cyber, women's and workers' rights).
- Tue, Thu — **legal news / law change** (new rule, notification, BNS/BNSS/BSA change, important government legal scheme).
- Sat — **"Kanoon ka fact" / myth-buster** on a common legal misconception, tied to a current case where possible.

Prefer stories with clear public value. Avoid: political-party controversies, ongoing protest cases, celebrity gossip, anything that names or identifies a victim of a sexual offence or a child (BNS s.72 / POCSO s.23), and pending matters where the court has not decided anything yet.

## 3. Verify (non-negotiable)
- Fetch the actual report (LiveLaw, Bar & Bench, Verdictum, SCC Online blog, court website). For judgments, record: case title, bench, date or citation, what was held, outcome.
- Every fact on the slides must be on the source page. If something isn't stated (e.g. date of order), leave it out rather than guess.
- Any section number you add (e.g. BNS/BNSS/BSA equivalents) must be one you are certain of; otherwise omit it.
- Write everything in your own words. Never copy sentences from the source.

## 4. Write `post.json`
Format exactly like the previous days' files: `date`, `topic`, `sources` (URLs), `slides`, `caption`.
- 6 slides: `cover` (kicker, title, subtitle, cite) → 3–4 `content` slides (label, title, 2–3 bullets, optional `note` for a "Kanoon ka fact") → `cta`.
- Use `**word**` for brass emphasis; keep each bullet under ~30 words; titles under ~8 words.
- If a ruling could be misread (e.g. "drugs are now legal"), add a "Dhyan rahe" slide that corrects it.
- Last content slide or caption must include: "Yeh post sirf jaankari ke liye hai, legal advice nahi."
- **Bar Council Rule 36:** no phone numbers, no "contact me for your case", no fees, no claims of success. Educational CTA only (follow / save / share).
- Caption: hook line + emoji, 3 short paragraphs, the citation line, the disclaimer, "Save karein 🔖 | Share karein 📤 | Follow @legalwithdigvijay", then 12–15 relevant hashtags (always include #LegalWithDigvijay #LegalAwareness #KanoonKiBaat). Max 2,200 characters and 30 hashtags.

## 5. Render and check
- `python3 tools/render.py posts/DATE/post.json posts/DATE` → `01.jpg` … `06.jpg`.
- Make a contact sheet (3×2, 540×675 each) and **look at it** with Read. Fix any text overflowing into the footer, awkward wraps, or typos, and re-render.
- Commit `post.json`, `caption.txt` and the JPEGs to `main` and push (end the commit message with the Co-Authored-By line).

## 6. Ask for approval
Send Digvijay (status `proactive`):
- the contact sheet with `SendUserFile`;
- a `SendUserMessage` with: the topic and source in one line, the full caption, and "Reply **approve** to publish now, or tell me what to change."

Then stop and wait for his reply in this session.

## 7. Publish (only after "approve")
Run the Make scenario **7937189** with `mcp__Make__scenarios_run` (`responsive: true`) and data:
```json
{
  "caption": "<caption text>",
  "ig_files": [{"media_type": "IMAGE", "image_url": "https://raw.githubusercontent.com/advdigvijay55-lang/legalwithdigvijay-posts/main/posts/DATE/01.jpg"}, ...],
  "fb_photos": [{"type": "url", "url": "<same URL>"}, ...]
}
```
Include every slide, in order. If the run fails, call `mcp__Make__executions_get-detail`, tell him the exact error in one line, and don't retry more than once. On success, confirm in one line that it's live on Instagram and Facebook.

If he asks for changes, edit `post.json`, re-render, push, and send the new preview before publishing.
