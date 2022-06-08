from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Nihaal=Client(
    "Pyrogram Bot",
    bot_token="5541342240:AAFvlATqafF1FB7TtMAMNVqdOv04c1a7nuY",
    api_id="18850696",
    api_hash="e3f5a7b4ea28b5c7ce9fc65e48274ae6"
)
START_MESSAGE= """
Hey {} How are you buddy
"""

@Nihaal.on_message(filters.command("start"))
async def start_message(Nihaal,message):
    await message.reply_photo(
        photo="https://telegra.ph/file/3f5c3a461d41522a3b7d2.jpg",
        caption=START_MESSAGE.fromat(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/NL_MP4"),
            InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/movie_lookam")
            ],[
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")
            ]]
         )
    )
        
            
    
    
Nihaal.run()
