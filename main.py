from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
import os
from db import LikeDB

TOKEN=os.environ.get('TOKEN')
likeDB = LikeDB('data.json')

def start(update: Update, context: CallbackContext):
    bot=context.bot
    chat_id=update.message.chat.id
    likeDB.add_student(str(chat_id))
    bot.sendMessage(chat_id,'Send me picture!')

def photo(updete: Update, context: CallbackContext):
    bot=context.bot
    chat_id=updete.message.chat.id
    photo=updete.message.photo[-1]['file_id']
    like = likeDB.all_likes(str(chat_id))
    dislike = likeDB.all_dislikes(str(chat_id))
    btn1 = InlineKeyboardButton(text=f'\U0001F44D {like}', callback_data="like")
    btn2 = InlineKeyboardButton(text=f'\U0001F44E {dislike}', callback_data="dislike")

    keyboard = InlineKeyboardMarkup([[btn1, btn2]])
    bot.sendPhoto(chat_id=chat_id, photo=photo, reply_markup=keyboard)

def count_like_dislike(update, context):
    query = update.callback_query
    data = query.data

    chat_id = query.message.chat.id
    if data=='like':
        query.answer(text='like😂')
        user_data=likeDB.add_like(str(chat_id))
    elif data=='dislike':
        query.answer(text='dislike😂')
        user_data = likeDB.add_dislike(str(chat_id))
    like =user_data['like']
    dislike=user_data['dislike']

    btn1 = InlineKeyboardButton(text=f'\U0001F44D {like}', callback_data="like")
    btn2 = InlineKeyboardButton(text=f'\U0001F44E {dislike}', callback_data='dislike')
    #query.answer(text='✅😂', show_alert=True)
    keyboard = InlineKeyboardMarkup([[btn1, btn2]])
    query.edit_message_reply_markup(reply_markup=keyboard)
updater = Updater(token=TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text, count_like_dislike))
dp.add_handler(MessageHandler(Filters.photo, photo))
dp.add_handler(CallbackQueryHandler(count_like_dislike))

updater.start_polling()
updater.idle()