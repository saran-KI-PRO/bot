import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# ✅ Get token from environment variable
TOKEN = os.getenv("8542542148:AAELATeMMg9jOA4qCMMVZe-KqfgBYu01r74")

# ❌ Stop if token missing
if TOKEN is None:
    print("ERROR: BOT_TOKEN not set")
    exit()

users = {}

# 🎯 Generate basic MCQs (you can upgrade to GPT later)
def generate_mcq(topic, n):
    questions = []
    answers = []

    for i in range(n):
        correct = random.choice(["A", "B", "C", "D"])

        questions.append({
            "q": f"{topic} Question {i+1}?",
            "options": [
                f"{topic} Option A",
                f"{topic} Option B",
                f"{topic} Option C",
                f"{topic} Option D"
            ]
        })

        answers.append(correct)

    return questions, answers


# ▶️ Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 Welcome to Quiz Bot!\n\n"
        "Send in this format:\n"
        "Topic: EEE, Questions: 5"
    )


# 📥 Handle quiz input
def start_quiz(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.chat_id

    try:
        parts = text.split(",")
        topic = parts[0].split(":")[1].strip()
        n = int(parts[1].split(":")[1].strip())

        questions, answers = generate_mcq(topic, n)

        users[user_id] = {
            "q": questions,
            "a": answers,
            "i": 0,
            "score": 0
        }

        send_question(user_id, context)

    except:
        update.message.reply_text("❌ Wrong format!\nUse: Topic: EEE, Questions: 5")


# 📤 Send question with buttons
def send_question(chat_id, context):
    data = users[chat_id]

    # 🎯 End condition
    if data["i"] >= len(data["q"]):
        score = data["score"]
        total = len(data["q"])

        context.bot.send_message(
            chat_id,
            f"🎯 Result:\nScore: {score}/{total}"
        )
        return

    q = data["q"][data["i"]]

    keyboard = [
        [InlineKeyboardButton("🅰️", callback_data="A"),
         InlineKeyboardButton("🅱️", callback_data="B")],
        [InlineKeyboardButton("🅲", callback_data="C"),
         InlineKeyboardButton("🅳", callback_data="D")]
    ]

    text = (
        f"📘 {q['q']}\n\n"
        f"A. {q['options'][0]}\n"
        f"B. {q['options'][1]}\n"
        f"C. {q['options'][2]}\n"
        f"D. {q['options'][3]}"
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔘 Handle button click
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id

    data = users[user_id]

    # ✅ Check answer
    if query.data == data["a"][data["i"]]:
        data["score"] += 1

    data["i"] += 1

    query.answer()

    send_question(user_id, context)


# 🚀 Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start_quiz))
    dp.add_handler(CallbackQueryHandler(button))

    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()


# ▶️ Run bot
if __name__ == "__main__":
    main()
