import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables
load_dotenv()

# Get the bot token from environment variables
API_TOKEN = os.getenv('BOT_TOKEN')
if API_TOKEN is None:
    raise ValueError("API_TOKEN is missing. Please set the BOT_TOKEN in your environment.")

# Initialize the bot with the API token
bot = telebot.TeleBot(API_TOKEN)

# Create 250 coupons
coupon_pool = [f'bibxatrizstudio-{str(i).zfill(3)}' for i in range(1, 251)]
available_coupons = set(coupon_pool)
user_coupons = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Generate a Coupon Code", callback_data="generate_coupon"))
    bot.send_message(message.chat.id, "Welcome! Click the button below to get your coupon code.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "generate_coupon")
def generate_coupon(call):
    user_id = call.from_user.id

    if user_id in user_coupons:
        bot.answer_callback_query(call.id, "You already generated your coupon code!")
        coupon = user_coupons[user_id]
    elif available_coupons:
        coupon = available_coupons.pop()
        user_coupons[user_id] = coupon
        bot.answer_callback_query(call.id, "Coupon generated successfully!")
    else:
        bot.answer_callback_query(call.id, "All coupon codes have been used.")
        bot.send_message(call.message.chat.id, "Sorry, all coupons are taken.")
        return

    # Instagram buttons
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("💐 Visit BunnyInBlooms Instagram", url="https://www.instagram.com/bunnyinblooms/")
    )
    markup.add(
        InlineKeyboardButton("📷 Visit Koreanatrizstudiosg Instagram", url="https://www.instagram.com/koreanatrizstudiosg/")
    )

    # Send coupon with Instagram buttons
    bot.send_message(call.message.chat.id, f"🎉 Your coupon code is: {coupon}", reply_markup=markup)

# Run the bot
bot.polling()
