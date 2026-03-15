# File memory for OpenCode

This project integrates new feature for OpenCode that dedicates one directory 
where OpenCode can store shared knwoledge. For example if user prefers some 
kind of code style. User can ask to list all file_memory and to store anything in file_memory.

Design:
- default shared directory file_memory is `~/Documents/opencode/file_memory`
- opencode has to decide what is optimal file format, "json" or "markdown"
- opencode has to decide how is this feature integrated to opencode itself? for exmaple as plain skill or even as 
speciaslised subagent who has this skill/feature enabled by deafault, so it can later run on local model

Implementation
- This skill is impelemented for owner of this PC exclusively, so you can do custom setup.
- Based on design Opencode plan and implements this feature and tests it.
- There is ollama available if you want it to use with small models prepared.
- You can ask for other resources if needed.
- To be clear you opencode is full product owner of this skill and 
make all decisions because youa re the one who know yourself the 
best, or atleast are able to efectively search your online documentation.

Notes:
Think I as user want to store in gfile_memory are for exampel progress of each project, long term goals, info 
about interesting tools i develop for you opencode so you can test them from other sessions. In plan to develop s lot 
of improvements and tools you can use but i will place them in separate projects so I want you to have
 one place where you can discover them as a starting point. Later we may replace file memory with something more 
sophisticated but it looks like useful basic tool I may want to keep in for simple stuff to store.
