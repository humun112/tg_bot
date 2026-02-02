import telebot

TOKEN = "8508236869:AAGtICkFBsqw_bdn3ek3wpTc-z4Px2rh_vE"
ADMIN_ID = 8336277978

bot = telebot.TeleBot(TOKEN)
user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте! Введите свой ИИН:")
    bot.register_next_step_handler(message, get_iin)


def get_iin(message):
    iin = message.text.strip()

    user_data[message.chat.id] = {"iin": iin}
    bot.send_message(message.chat.id, "Теперь отправьте номер телефона:")
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    phone = message.text.strip()


    user_data[message.chat.id]["phone"] = phone
    bot.send_message(message.chat.id, "Теперь введи номер водительских прав:")
    bot.register_next_step_handler(message, get_license)


def get_license(message):
    license_number = message.text.strip().upper()

    user_data[message.chat.id]["license"] = license_number

    bot.send_message(message.chat.id, "✅ Спасибо! Данные отправлены администратору.")

    username = message.from_user.username or "без username"

    bot.send_message(
        ADMIN_ID,
        f"📥 Новая заявка!\n\n"
        f"👤 Пользователь: @{username}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"📄 ИИН: {user_data[message.chat.id]['iin']}\n"
        f"📱 Телефон: {user_data[message.chat.id]['phone']}\n"
        f"🪪 Вод. права: {user_data[message.chat.id]['license']}"
    )


print("Бот запущен и работает...")
bot.remove_webhook()  # удаляет текущий вебхук
bot.polling(none_stop=True)  # запускает polling
bot.infinity_polling()

