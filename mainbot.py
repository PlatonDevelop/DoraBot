import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


TOKEN = ""
CONTACT = ""


main_menu_keyboard = [['🛒 Каталог'], ['🛍️ Сделать заказ'], ['ℹ️ Информация о боте и техподдержка']]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True)


catalog_menu_keyboard = [['🛍️ ---Категории Товаров---'], ['Юбки', 'Карсеты'], ['Топы', 'Аксесуары'], ['Сумки', 'Штаны'],
                         ['Платья', 'Комплекты'], ['🔙 Назад']]
catalog_menu_markup = ReplyKeyboardMarkup(catalog_menu_keyboard, one_time_keyboard=True)


info_menu_keyboard = [['🔙 Назад']]
info_menu_markup = ReplyKeyboardMarkup(info_menu_keyboard, one_time_keyboard=True)


first_time_menu_keyboard = [['Начать шоппинг 🎀']]
first_time_menu_markup = ReplyKeyboardMarkup(first_time_menu_keyboard, one_time_keyboard=True)


user_sessions = {}



async def start(update: Update, context) -> None:
    user_id = update.message.from_user.id
    user_first_name = update.message.from_user.first_name

    
    if user_id not in user_sessions:
        user_sessions[user_id] = True
        greeting_text = f"Здравствуйте, {user_first_name}, добро пожаловать в 4angels.store! 🎀"
        await update.message.reply_text(greeting_text, reply_markup=first_time_menu_markup)
    else:
        greeting_text = f"Здравствуйте, {user_first_name}, добро пожаловать обратно в 4angels.store! 🎀"
        await update.message.reply_text(greeting_text, reply_markup=main_menu_markup)



async def handle_first_time(update: Update, context) -> None:
    user_id = update.message.from_user.id
    if user_id in user_sessions:
        await update.message.reply_text("Выберите опцию ✨", reply_markup=main_menu_markup)



async def handle_menu(update: Update, context) -> None:
    text = update.message.text
    logger.debug(f"Обработка основного меню: {text}")

    if text == '🛒 Каталог':
        await update.message.reply_text(
            "Выберите товар ✨",
            reply_markup=catalog_menu_markup
        )
    elif text == '🛍️ Сделать заказ':
        await update.message.reply_text(
            f"Для оформления заказа, пожалуйста, обратитесь к: @{CONTACT}",
            reply_markup=ReplyKeyboardMarkup([['🔙 Назад']], one_time_keyboard=True)
        )
    elif text == 'ℹ️ Информация о боте и техподдержка':
        await update.message.reply_text(
            f"Разработчик бота: @platonnagy 🧑‍💻🎀 \n"
            f"По всем вопросам касающимся бота обращайтесь по контакту выше \n"
            f"По всем вопросам касающимся магазина, продаж, каталога обращайтесь по контакту @{CONTACT}\n"
            f"Бот создан с помощью PyCharm\n"
            f"Все права защищены ©️",
            reply_markup=info_menu_markup
        )



async def handle_catalog(update: Update, context) -> None:
    text = update.message.text
    logger.debug(f"Обработка каталога: {text}")

 
    if text == 'Юбки':
        await update.message.reply_text("Тут список юбок.", reply_markup=catalog_menu_markup)
    elif text == 'Карсеты':
        await update.message.reply_text("Тут список карсетов.", reply_markup=catalog_menu_markup)
    elif text == 'Топы':
        await update.message.reply_text("Тут список топов.", reply_markup=catalog_menu_markup)
    elif text == 'Аксесуары':
        await update.message.reply_text("Тут список аксессуаров.", reply_markup=catalog_menu_markup)
    elif text == 'Сумки':
        await update.message.reply_text("Тут список сумок.", reply_markup=catalog_menu_markup)
    elif text == 'Штаны':
        await update.message.reply_text("Тут список штанов.", reply_markup=catalog_menu_markup)
    elif text == 'Платья':
        await update.message.reply_text("Тут список платьев.", reply_markup=catalog_menu_markup)
    elif text == 'Комплекты':
        await update.message.reply_text("Тут список комплектов.", reply_markup=catalog_menu_markup)
    elif text == '🔙 Назад':
        await update.message.reply_text("Возвращаемся в главное меню", reply_markup=main_menu_markup)



def main():
    logger.debug("Запуск основного процесса")

   
    application = Application.builder().token(TOKEN).build()

   
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^Начать шоппинг 🎀$'), handle_first_time))
    application.add_handler(
        MessageHandler(filters.Regex('^(🛒 Каталог|🛍️ Сделать заказ|ℹ️ Информация о боте и техподдержка)$'),
                       handle_menu))
    application.add_handler(
        MessageHandler(filters.Regex('^(Юбки|Карсеты|Топы|Аксесуары|Сумки|Штаны|Платья|Комплекты|🔙 Назад)$'),
                       handle_catalog))

   
    application.run_polling()


if __name__ == '__main__':
    main()





