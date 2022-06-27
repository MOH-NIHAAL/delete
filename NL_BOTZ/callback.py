import asyncio
import re
import ast
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from DB.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, CH_FILTER, CH_LINK
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, split_list, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from DB.users_chats_db import db
from DB.ia_filterdb import Media, get_file_details, get_filter_results
from DB.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message(filters.group & filters.text & ~filters.edited & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)

@Client.on_callback_query()
async def cb_handler(client: Client, query):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id

    if (clicked == typed):

# # ---------- 🔘 [ | 𝗚𝗥𝗢𝗨𝗣 𝗙𝗜𝗟𝗧𝗘𝗥𝗦 | ] 🔘 ---------- # #
        if query.data.startswith("nextgroup"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("This Is My Old Message So Please Request Again 🙏",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                     [InlineKeyboardButton("🔙 Back Page", callback_data=f"backgroup_{int(index)+1}_{keyword}"),
                      InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )            
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"backgroup_{int(index)+1}_{keyword}"),InlineKeyboardButton("Next Page ➡", callback_data=f"nextgroup_{int(index)+1}_{keyword}")]
                )        
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

        elif query.data.startswith("backgroup"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("This Is My Old Message So Please Request Again 🙏",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("Next Page ➡", callback_data=f"nextgroup_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="Check PM", url=f"https://telegram.dog/{bot_info.BOT_USERNAME}")]
                )
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"backgroup_{int(index)-1}_{keyword}"),InlineKeyboardButton("Next Page ➡", callback_data=f"nextgroup_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="Check PM", url=f"https://telegram.dog/{bot_info.BOT_USERNAME}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            
@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("⚠️ Bʀᴏ ꜱᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ ғɪʟᴇ . Dᴏɴ'ᴛ ʀᴇǫᴜᴇꜱᴛ ᴏᴛʜᴇʀꜱ ғɪʟᴇ 😩", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("Aʜʜ... Bᴜᴛᴛᴏɴ Exᴘɪʀᴇᴅ Pʟᴇᴀsᴇ Rᴇǫᴜᴇsᴛ Aɢᴀɪɴ 🙂", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('𝙲𝙷𝙴𝙲𝙺𝙸𝙽𝙶 𝙵𝙸𝙻𝙴 𝙾𝙽 𝙼𝚈 𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('𝚃𝙷𝙸𝚂 𝙼𝙾𝚅𝙸𝙴 I𝚂 𝙽𝙾𝚃 𝚈𝙴𝚃 𝚁𝙴𝙻𝙴𝙰𝚂𝙴𝙳 𝙾𝚁 𝙰𝙳𝙳𝙴𝙳 𝚃𝙾 𝙳𝙰𝚃𝚂𝙱𝙰𝚂𝙴 💌')
            await asyncio.sleep(10)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return
        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
 
        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
            size = size
            mention = mention
        if f_caption is None:
            f_caption = f"{files.file_name}"
            size = f"{files.file_size}"
            mention = f"{query.from_user.mention}"
        buttons = [
            [
                InlineKeyboardButton('『🎪 ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ 🎪』', url='https://t.me/movie_lookam')
            ]
            ]

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                ms = await client.send_cached_media(
                    chat_id=CH_FILTER,
                    file_id=file_id,
                    caption=f'<b>ʜᴇʏ 👋 {query.from_user.mention} 😊</b>\n\n<b>🗂️ ɴᴀᴍᴇ : <a href=https://t.me/movie_lookam>{title}</a></b>\n\n<b>⚙️ sɪᴢᴇ : {size}</b>\n\n<i>⚠️ 𝐓𝐡𝐢𝐬 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐖𝐢𝐥𝐥 𝐁𝐞 𝐀𝐮𝐭𝐨-𝐃𝐞𝐥𝐞𝐭𝐞𝐝 𝐈𝐧 𝐍𝐞𝐱𝐭 𝟓 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐓𝐨 𝐀𝐯𝐨𝐢𝐝 𝐂𝐨𝐩𝐲𝐫𝐢𝐠𝐡𝐭 𝐈𝐬𝐬𝐮𝐞𝐬.𝐒𝐨 𝐅𝐨𝐫𝐰𝐚𝐫𝐝 𝐓𝐡𝐢𝐬 𝐅𝐢𝐥𝐞 𝐓𝐨 𝐀𝐧𝐲𝐰𝐡𝐞𝐫𝐞 𝐄𝐥𝐬𝐞 𝐁𝐞𝐟𝐨𝐫𝐞 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠.. ⚠️</i>\n\n<b>🧑🏻‍💻 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {query.from_user.mention}\n🚀 ɢʀᴏᴜᴘ : {query.message.chat.title}</b>',
                    reply_markup = InlineKeyboardMarkup(buttons),
                    protect_content=True if ident == "filep" else False 
                )
                msg1 = await query.message.reply(
                f'<b> ʜᴇʏ 👋 {query.from_user.mention} </b>😍\n\n<b>📫 ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ 📥</b>\n\n'           
                f'<b>📂 Fɪʟᴇ Nᴀᴍᴇ</b> : <code>[CL] {title}</code>\n\n'              
                f'<b>⚙️ Fɪʟᴇ Sɪᴢᴇ</b> : <b>{size}</b>',
                True,
                'html',
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📥  ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ  📥", url = ms.link)
                        ],
                        [
                            InlineKeyboardButton("⚠️ ᴄᴀɴɴᴏᴛ ᴀᴄᴄᴇss ❓ ᴄʟɪᴄᴋ ʜᴇʀᴇ ⚠️", url = f"{CH_LINK}")
                        ]
                    ]
                )
            )
            await asyncio.sleep(600)
            await msg1.delete()            
            await ms.delete()
            del msg1, ms
        except Exception as e:
            logger.exception(e, exc_info=True)

    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer(f"☆ 𝐇𝐄𝐘 𝐈 𝐋𝐈𝐊𝐄 𝐘𝐎𝐔𝐑 𝐒𝐌𝐀𝐑𝐓𝐍𝐄𝐒 ! 𝐁𝐔𝐓 𝐃𝐎𝐍𝐓 𝐁𝐄 𝐎𝐕𝐄𝐑𝐒𝐌𝐀𝐑𝐓 😏",show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            await query.answer(f"🦋 ʜᴇʟʟᴏ ᴍʏ ғʀɪᴇɴᴅ ᴘʟᴇᴀsᴇ sᴇɴᴛ ʀᴇǫᴜᴇsᴛ ᴀɢᴀɪɴ 🦋",show_alert=True)
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        buttons = [
            [
                InlineKeyboardButton('『🎪 ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ 🎪』', url='https://t.me/movie_lookam')
            ]
            ]
        await query.answer()
        await client.send_cached_media(
            chat_id=CH_FILTER,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
        InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/CL_FILTER_BOT?startgroup=true')
        ], [
        InlineKeyboardButton('⚙️ ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('😊 ᴀʙᴏᴜᴛ', callback_data='about_menu')
        ], [
        InlineKeyboardButton("🔖 sᴜᴘᴘᴏʀᴛ", url='https://t.me/NL_BOTxCHAT')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup
        )
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Filters', callback_data='filter'),
            InlineKeyboardButton('Info', callback_data='info')
        ], [
            InlineKeyboardButton('Connection', callback_data='coct'),
            InlineKeyboardButton('IMDb', callback_data='omdb')
        ], [
            InlineKeyboardButton('« Back', callback_data='start'),
            InlineKeyboardButton('Status', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup
        )
    elif query.data == "about_menu":
        buttons = [[
        InlineKeyboardButton('📊 sᴛᴀᴛᴜs', callback_data='stats'),
        InlineKeyboardButton('📚 ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('🏡 ʜᴏᴍᴇ', callback_data='start')
        ],[
        InlineKeyboardButton('⛔️ ᴄʟɪᴄᴋ ᴛᴏ ᴄʟᴏsᴇ ᴘᴀɢᴇs ⛔️', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='filter'),
            InlineKeyboardButton('Button', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "filter":
        buttons = [[
            InlineKeyboardButton('Manual Filter', callback_data='manuelfilter'),
            InlineKeyboardButton('Auto Filter', callback_data='autofilter')
        ],[
            InlineKeyboardButton('« Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="**Choose your Desired Filter**",
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "info":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='help'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.INFO_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "omdb":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.IMDB_TXT,
            reply_markup=reply_markup,
            parse_mode='md'
        )
    elif query.data == "close":
        await query.message.delete()
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('« Back', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('Refresh', callback_data='rfrsh'),
            InlineKeyboardButton('« Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching...")
        buttons = [[
            InlineKeyboardButton('Refresh', callback_data='rfrsh'),
            InlineKeyboardButton('« Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "reason":
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ⪼ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ⪼ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ⪼ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴋɢꜰ ᴄʜᴀᴘᴛᴇʀ 2  2022\n\n✘ ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© Tʜᴏᴍᴀs Sʜᴇʟʙʏ", show_alert=True)
    
    elif query.data == "movss":
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ⪼ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ⪼ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ⪼ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴋɢꜰ ᴄʜᴀᴘᴛᴇʀ 2  2022\n\n✘ ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© Tʜᴏᴍᴀs Sʜᴇʟʙʏ", show_alert=True)

    elif query.data == "moviis":  
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ⪼ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ⪼ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ⪼ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ʟᴏᴋɪ S01 E01\n\n✘ ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© Tʜᴏᴍᴀs Sʜᴇʟʙʏ", show_alert=True)   
    
    elif query.data == 'reqst1':
        await query.answer("Hey Bro 😍\n\n🎯 Click On The Button below The Files You Want  ⬇️", show_alert=True)
    
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)


async def auto_filter(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            btn.append([InlineKeyboardButton(f'📁 {search} 📁', 'reqst1')]
            )
            btn.append([InlineKeyboardButton(f'ғɪʟᴇs: {len(files)}', 'reqst1'),
                       InlineKeyboardButton(f'ᴍᴏᴠɪᴇ', 'movss'),
                       InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ', 'moviis')]
            )
            for file in files:
                file_id = file.file_id
                file_name = file.file_name
                file_size = get_size(file.file_size)
                btn.append([InlineKeyboardButton(text=f'🍭 {file_name}', callback_data=f"files#{file_id}"),
                            InlineKeyboardButton(text=f'🍬 {file_size}', callback_data=f"files#{file_id}")]
                )
        else:
            if SPELL_CHECK_REPLY:  
                reply = search.replace(" ", "+")
                reply_markup = InlineKeyboardMarkup([[
                 InlineKeyboardButton("🔮IMDB🔮", url=f"https://imdb.com/find?q={reply}"),
                 InlineKeyboardButton("🪐 Reason", callback_data="reason")
                 ]]
                )    
                imdb=await get_poster(search)
                if imdb and imdb.get('poster'):
                    await message.reply_photo(photo=imdb.get('poster'), caption=script.IMDB_MOVIE_2.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url'], short=imdb['short_info']), reply_markup=reply_markup) 
                    return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages"),
                 InlineKeyboardButton("Close 🗑️", callback_data="close")]
            )

            imdb=await get_poster(search)
            if imdb and imdb.get('poster'):
                await message.reply_photo(photo=imdb.get('poster'), caption=script.IMDB_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url'], short=imdb['short_info']), reply_markup=InlineKeyboardMarkup(buttons))
            elif imdb:
                await message.reply_photo(photo=imdb.get('poster'), caption=script.IMDB_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url'], short=imdb['short_info']), reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_sticker("CAACAgUAAxkBAAIBPWJukSYrqGzTevtJeiXt0VurpiW0AALjBQACpKMQVP3FLTCQDGE0JAQ", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="Next Page ➡",callback_data=f"nextgroup_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton("Close 🗑️", callback_data="close")]
        )
        
        imdb=await get_poster(search)
        if imdb and imdb.get('poster'):
            await message.reply_photo(photo=imdb.get('poster'), caption=script.IMDB_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url'], short=imdb['short_info']), reply_markup=InlineKeyboardMarkup(buttons))
        elif imdb:
            await message.reply_photo(photo=random.choice(BOT_PICS), caption=script.IMDB_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url'], short=imdb['short_info']), reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_sticker("CAACAgUAAxkBAAIBPWJukSYrqGzTevtJeiXt0VurpiW0AALjBQACpKMQVP3FLTCQDGE0JAQ", reply_markup=InlineKeyboardMarkup(buttons))

            
async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
