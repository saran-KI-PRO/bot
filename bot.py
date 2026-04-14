from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import random
import os

TOKEN = os.grtenv("8542542148:AAELATeMMg9jOA4qCMMVZe-KqfgBYu01r74")

users = {}

def generate_mcq(topic, n):
    questions = []
    answers = []

    for i in range(n):
        correct = random.choice(["A", "B", "C", "D"])
        questions.append({
            "q": f"{topic} Question {i+1}?",
            "options": ["Option A", "Option B", "Option C", "Option D"]
        })
        answers.append(correct)

    return questions, answers


def start(update, context):
    update.message.reply_text("Send:\nTopic: EEE, Questions: 5")


def start_quiz(update, context):
    text = update.message.text
    user_id = update.message.chat_id

    try:
        parts = text.split(",")
        topic = parts[0].split(":")[1].strip()
        n = int(parts[1].split(":")[1].strip())

        q, a = generate_mcq(topic, n)

        users[user_id] = {
            "q": q,
            "a": a,
            "i": 0,
            "score": 0
        }

        send_q(user_id, context)

    except:
        update.message.reply_text("Wrong format ❌")


def send_q(chat_id, context):
    data = users[chat_id]

    if data["i"] >= len(data["q"]):
        score = data["score"]
        total = len(data["q"])

        context.bot.send_message(chat_id, f"Score: {score}/{total}")
        return

    q = data["q"][data["i"]]

    keyboard = [
        [InlineKeyboardButton("A", callback_data="A"),
         InlineKeyboardButton("B", callback_data="B")],
        [InlineKeyboardButton("C", callback_data="C"),
         InlineKeyboardButton("D", callback_data="D")]
    ]

    context.bot.send_message(
        chat_id,
        f"{q['q']}\nA. {q['options'][0]}\nB. {q['options'][1]}\nC. {q['options'][2]}\nD. {q['options'][3]}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def button(update, context):
    query = update.callback_query
    user_id = query.message.chat_id

    data = users[user_id]

    if query.data == data["a"][data["i"]]:
        data["score"] += 1

    data["i"] += 1

    query.answer()
    send_q(user_id, context)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, start_quiz))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


main()
