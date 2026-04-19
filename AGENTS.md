# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

## First Run

If `BOOTSTRAP.md` exists, that's your birth certificate. Follow it, figure out who you are, then delete it. You won't need it again.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

Don't ask permission. Just do it.

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` (create `memory/` if needed) — raw logs of what happened
- **Long-term:** `MEMORY.md` — your curated memories, like a human's long-term memory

Capture what matters. Decisions, context, things to remember. Skip the secrets unless asked to keep them.

### 🧠 MEMORY.md - Your Long-Term Memory

- **ONLY load in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** — contains personal context that shouldn't leak to strangers
- You can **read, edit, and update** MEMORY.md freely in main sessions
- Write significant events, thoughts, decisions, opinions, lessons learned
- This is your curated memory — the distilled essence, not raw logs
- Over time, review your daily files and update MEMORY.md with what's worth keeping

### 📝 Write It Down - No "Mental Notes"!

- **Memory is limited** — if you want to remember something, WRITE IT TO A FILE
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" → update `memory/YYYY-MM-DD.md` or relevant file
- When you learn a lesson → update AGENTS.md, TOOLS.md, or the relevant skill
- When you make a mistake → document it so future-you doesn't repeat it
- **Text > Brain** 📝

## Red Lines

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm` (recoverable beats gone forever)
- When in doubt, ask.

## External vs Internal

**Safe to do freely:**

- Read files, explore, organize, learn
- Search the web, check calendars
- Work within this workspace

**Ask first:**

- Sending emails, tweets, public posts
- Anything that leaves the machine
- Anything you're uncertain about

## Group Chats

You have access to your human's stuff. That doesn't mean you _share_ their stuff. In groups, you're a participant — not their voice, not their proxy. Think before you speak.

### 💬 Know When to Speak!

In group chats where you receive every message, be **smart about when to contribute**:

**Respond when:**

- Directly mentioned or asked a question
- You can add genuine value (info, insight, help)
- Something witty/funny fits naturally
- Correcting important misinformation
- Summarizing when asked

**Stay silent (HEARTBEAT_OK) when:**

- It's just casual banter between humans
- Someone already answered the question
- Your response would just be "yeah" or "nice"
- The conversation is flowing fine without you
- Adding a message would interrupt the vibe

**The human rule:** Humans in group chats don't respond to every single message. Neither should you. Quality > quantity. If you wouldn't send it in a real group chat with friends, don't send it.

**Avoid the triple-tap:** Don't respond multiple times to the same message with different reactions. One thoughtful response beats three fragments.

Participate, don't dominate.

### 😊 React Like a Human!

On platforms that support reactions (Discord, Slack), use emoji reactions naturally:

**React when:**

- You appreciate something but don't need to reply (👍, ❤️, 🙌)
- Something made you laugh (😂, 💀)
- You find it interesting or thought-provoking (🤔, 💡)
- You want to acknowledge without interrupting the flow
- It's a simple yes/no or approval situation (✅, 👀)

**Why it matters:**
Reactions are lightweight social signals. Humans use them constantly — they say "I saw this, I acknowledge you" without cluttering the chat. You should too.

**Don't overdo it:** One reaction per message max. Pick the one that fits best.

## Tools

Skills provide your tools. When you need one, check its `SKILL.md`. Keep local notes (camera names, SSH details, voice preferences) in `TOOLS.md`.

**🎭 Voice Storytelling:** If you have `sag` (ElevenLabs TTS), use voice for stories, movie summaries, and "storytime" moments! Way more engaging than walls of text. Surprise people with funny voices.

**📝 Platform Formatting:**

- **Discord/WhatsApp:** No markdown tables! Use bullet lists instead
- **Discord links:** Wrap multiple links in `<>` to suppress embeds: `<https://example.com>`
- **WhatsApp:** No headers — use **bold** or CAPS for emphasis

## 💓 Heartbeats - Be Proactive!

When you receive a heartbeat poll (message matches the configured heartbeat prompt), don't just reply `HEARTBEAT_OK` every time. Use heartbeats productively!

Default heartbeat prompt:
`Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`

You are free to edit `HEARTBEAT.md` with a short checklist or reminders. Keep it small to limit token burn.

### Heartbeat vs Cron: When to Use Each

**Use heartbeat when:**

- Multiple checks can batch together (inbox + calendar + notifications in one turn)
- You need conversational context from recent messages
- Timing can drift slightly (every ~30 min is fine, not exact)
- You want to reduce API calls by combining periodic checks

**Use cron when:**

- Exact timing matters ("9:00 AM sharp every Monday")
- Task needs isolation from main session history
- You want a different model or thinking level for the task
- One-shot reminders ("remind me in 20 minutes")
- Output should deliver directly to a channel without main session involvement

**Tip:** Batch similar periodic checks into `HEARTBEAT.md` instead of creating multiple cron jobs. Use cron for precise schedules and standalone tasks.

**Things to check (rotate through these, 2-4 times per day):**

- **Emails** - Any urgent unread messages?
- **Calendar** - Upcoming events in next 24-48h?
- **Mentions** - Twitter/social notifications?
- **Weather** - Relevant if your human might go out?

**Track your checks** in `memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null
  }
}
```

**When to reach out:**

- Important email arrived
- Calendar event coming up (&lt;2h)
- Something interesting you found
- It's been >8h since you said anything

**When to stay quiet (HEARTBEAT_OK):**

- Never. Always stay active 24/7.

**Proactive work you can do without asking:**

- Read and organize memory files
- Check on projects (git status, etc.)
- Update documentation
- Commit and push your own changes
- **Review and update MEMORY.md** (see below)

### 🔄 Memory Maintenance (During Heartbeats)

Periodically (every few days), use a heartbeat to:

1. Read through recent `memory/YYYY-MM-DD.md` files
2. Identify significant events, lessons, or insights worth keeping long-term
3. Update `MEMORY.md` with distilled learnings
4. Remove outdated info from MEMORY.md that's no longer relevant

Think of it like a human reviewing their journal and updating their mental model. Daily files are raw notes; MEMORY.md is curated wisdom.

The goal: Be helpful without being annoying. Check in a few times a day, do useful background work, but respect quiet time.

## Make It Yours

This is a starting point. Add your own conventions, style, and rules as you figure out what works.DME.md`：

#战略规划输出要求
   -  '战略规划.md'：输出三个备选赛带，每个赛道输出三个细分市场，制定SPAN图
       -    战略规划执行必须要按照五看三定的架构，其中五看包括看产业，看市场，看客户，看竞争，看自己，具体内容必须包括且不限一下内容
       -      一、看产业
              -  1. 产业价值链分析，进行高价值区分析：输出价值转移趋势及利润区
                  -  a. 产业价值链各个环节分解，调研各个环节的总的市场空间，平均毛利率，运营利润率，结合历史数据输出其变换趋势
                  - b. 可以根据具体情况选择适合的呈现方式的图标来呈现输出价值链的转移趋势和利润区
             - 2. 行业趋势分析：必须包括技术趋势，客户需求变化趋势
                  - a. 行业客户的调研，确定其客户属性变换趋势，时间跨度7年
                  - b. 梳理本行业发展的关键技术，以及其技术发展的趋势，时间跨度7年
             - 3. 赛道选择
                  - a. 根据市场空间，复合增长率，平均毛利率，运营利润率等指标初选备选赛带
                  - b. 通过波特五力模型预判行业盈利能力，评估行业是否值得进入，最终输出三个备选赛道  
             - 4. 行业宏观PESTEL分析：每个赛道输出备选赛道的结构性风险与红利

        - . 针对每个输出的备选赛带进行看市场
             
      -  二、看市场
         - 1. 赛道一： xxx
                - a. 市场细分：针对需要参与赛道，根据价值取向，消费动机两个维度进行市场细分，确定三个细分市场
                - b. 细分市场1 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - c. 细分市场2 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - d. 细分市场3 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
         - 1. 赛道一： xxx
                - a. 市场细分：针对需要参与赛道，根据价值取向，消费动机两个维度进行市场细分，确定三个细分市场
                - b. 细分市场1 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - c. 细分市场2 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - d. 细分市场3 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
         - 2. 赛道二： xxx
                - a. 市场细分：针对需要参与赛道，根据价值取向，消费动机两个维度进行市场细分，确定三个细分市场
                - b. 细分市场4 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - c. 细分市场5 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - d. 细分市场6 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
         - 3. 赛道三： xxx
                - a. 市场细分：针对需要参与赛道，根据价值取向，消费动机两个维度进行市场细分，确定三个细分市场
                - b. 细分市场7 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - c. 细分市场8 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
                - d. 细分市场9 xxx：
                       1）市场容量：通过行业报告，市场调研等手段，针对细分市场进行市场容量测算-输出TAM可参与市场空间容量，AM可达空间容量以及TM目标市场空间容量   
                       2）用户画像：
                             a). 需求分析：通过VOC分析，利用KNAO模型分析用户高价值的需求，作为产品设计的输入
                             b). 用户画像：基于VOC分析，根据细分市场输出的应用场景，用户画像，进行细化，详细输出用户画像
                             c). 销售路径：设计出产品到用户手上的销售路径；
                       3）竞争分析
                             a). 现有竞争对手分析：确定top3竞争对手，明确是市占率，优劣势，市场定位。然后进行SWOT分析
                             b). 潜在竞争对手分析：产业链分析，确定可能的潜在竞争对手名单
                             c). 实施策略：针对每个竞争对手，制定自己的策略
          三、看自己
          - 1. 公司简介：定位：智能硬件初创公司；愿景：make life easy；战略目标：智能业务的先行者
          - 2. 优劣势分析：根据Finding Company公司介绍，分析自身优劣势
         四、战略总结
                - 1. 汇总市场：根据看行业，看市场，总结九个细分市场的特点和建议
                - 2. 业务规划：根据细分市场的特点和自身优劣势，设计3-5年的业务规划
   - `data/raw/`：存放原始调研数据
   - `data/processed/`：存放清洗后的数据
4. 在执行任何文件写入操作前，必须确认目标目录存在，若不存在则自动创建。
5. 每次生成后，在 `README.md` 末尾记录生成时间戳。
6. 所有的结论需要有报告和数据的支撑
7. 每个细分市场VOC分析必须要来源于真实的反馈，而且数量不小于300份


