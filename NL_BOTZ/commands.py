from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


START_MESSAGE= """
Hey {} How are you buddy
"""

@Nihaal.on_message(filters.command("start"))
async def start_message(Nihaal,message):
    await message.reply_photo(
        photo="https://telegra.ph/file/3f5c3a461d41522a3b7d2.jpg",
        caption=START_MESSAGE.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/NL_MP4"),
            InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/movie_lookam")
            ],[
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")
            ]]
         )
    )
    
@Nihaal.on_message(filters.command("info"))
async def info(bot, msg):
    text = f"""
𝙵𝙸𝚁𝚂𝚃 𝙽𝙰𝙼𝙴 = {msg.from_user.first_name}
𝙻𝙰𝚂𝚃 𝙽𝙰𝙼𝙴 = {msg.from_user.last_name}
𝚄𝚂𝙴𝚁𝙽𝙰𝙼𝙴 = @{msg.from_user.username}
𝚄𝚂𝙴𝚁 𝙸𝙳 = {msg.from_user.id}
𝙻𝙸𝙽𝙺 = {msg.from_user.mention}
"""
    await msg.reply_text(text=text)
        
            
    
    
Nihaal.run()
