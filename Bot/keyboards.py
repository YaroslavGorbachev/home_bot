from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_1 = KeyboardButton('Продолжить')
greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_1)
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1)