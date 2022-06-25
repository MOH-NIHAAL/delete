class script(object):
    START_TXT = """Hey {}"""
    HELP_TXT = """Help {}"""
    ABOUT_TXT = """About"""
    IMDB_MOVIE_2 = """
🎬 **Title** : [{title}]({url})
🎭 **Genre** : {genres}
📆 **Release** : {year}
📕 **Short Info** : {short}
"""
    IMDB_MOVIE_1 = """
🎬 **Title** : [{title}]({url})
🎭 **Genre** : {genres}
📆 **Release** : {year}
📕 **Short Info** : {short}
"""
    MANUELFILTER_TXT = """**Filters**
- Filter is the feature were users can set automated replies for a particular keyword and EvaMaria will respond whenever a keyword is found the message

**NOTE:**
1. Bot should have admin privilege on the chat
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.

**Commands and Usage:**
• /filter - add a filter in chat
• /filters - list all the filters of a chat
• /del - delete a specific filter in chat
• /delall - delete the whole filters in a chat (chat owner only)"""

    BUTTON_TXT = """**Buttons**
- @Zac_AutoFilterBot Support both url and alert inline buttons.

**URL buttons:**
`[Button Text](buttonurl:https://t.me/EvaMariaBot)`
Alert buttons:
`[Button Text](buttonalert:This is an alert message)`"""

    AUTOFILTER_TXT = """**Autofilter**
Autofilter is the feature in which the bot provides the files stored in its database to the users based on their queries in the form of auto generated button filters.
Currently the Autofilter provides movie & series files to users in respect of their queries.

**COMMANDS & USAGE:**
• /settings: To adjust the Autofilter settings specific to your group.

**NOTE:**
- To adjust the Autofilter settings make sure that you have connected your group to my PM. If not then you can do so by using the command /connect .
- If you don't know the group id you can access it by giving the command /id in your group."""

    CONNECTION_TXT = """**Connections**
- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.

**Commands and Usage:**
• /connect  - connect a particular chat to your PM
• /disconnect  - disconnect from a chat
• /connections - list all your connections"""
    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>NOTE:</b>
these are the extra features of Eva Maria

<b>Commands and Usage:</b>
• /id - <code>get id of a specified user.</code>
• /info  - <code>get information about a user.</code>
• /imdb  - <code>get the film information from IMDb source.</code>
• /search  - <code>get the film information from various sources.</code>"""
    ADMIN_TXT = """Help: <b>Admin mods</b>

<b>NOTE:</b>
This module only works for my admins

<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""
    STATUS_TXT = """★ 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃𝚂: <code>{}</code>
★ 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱
★ 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱"""
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""
    INFO_TXT = """**Info**
- You can get a Telegram **ID** of any users or a specified user on a group or Bots PM.

**Command & Usage:**
• /info - To Search a Movie Info
• /id - To Search Something about Something

"""
    IMDB_TXT = """**IMDb**
- This is an awsom feature to **Search** About a movie Detail without leaving Telegram

**Command & Usage:**
• /IMDb - To Search a Movie Info
• /Search - To Search Something about Something
"""
