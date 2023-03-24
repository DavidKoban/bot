# coding=utf8
import json
import sys
import time
from telebot import types, TeleBot
from binance.client import Client

bot = TeleBot('6194383536:AAFwd6NRzlMJnG9PSqT0SBITAMSGp9zJONY')
bot_manager = TeleBot('5767387114:AAGB6MSt5W33XqKqqnXF74Qt46cwyal8d94')
bot.set_webhook()


def get_curses():
    global curses
    f = json.load(open("curses.txt", "r"))
    client = Client(f['client']['key'], f['client']['secret'])
    fee = f['fee']
    curses = {
        'BTCSELL': float(client.get_ticker(symbol='BTCUSDT')['lastPrice']) * (1 - fee),
        'ETHSELL': float(client.get_ticker(symbol='ETHUSDT')['lastPrice']) * (1 - fee),
        'USDTSELL': 1 * (1 - fee),
        'BTCBUY': float(client.get_ticker(symbol='BTCUSDT')['lastPrice']) * (1 + fee),
        'ETHBUY': float(client.get_ticker(symbol='ETHUSDT')['lastPrice']) * (1 + fee),
        'USDTBUY': 1 * (1 + fee),
    }


try:
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.from_user.id, "*Привет, "+message.from_user.first_name+"👋🏻!*\n\nДобро пожаловать в Binance exchange dxb — ваш бытрый криптообменник.", parse_mode='Markdown')
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Обмен криптовалюты 💱')
        itembtn2 = types.KeyboardButton('Обменные курсы 📊')
        itembtn3 = types.KeyboardButton('Поддержка ☎')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.from_user.id, "*Выберите действие:*", reply_markup=markup, parse_mode='Markdown')
        if message.from_user.id == 266284325:
            button1 = types.InlineKeyboardButton("Изменить API", callback_data='1a')
            button2 = types.InlineKeyboardButton("Изменить крипто кошельки", callback_data='2a')
            button3 = types.InlineKeyboardButton("Изменить карту для оплаты", callback_data='3a')
            button4 = types.InlineKeyboardButton("Изменить PayPal", callback_data='4a')
            button5 = types.InlineKeyboardButton("Изменить комисиию", callback_data='5a')
            button6 = types.InlineKeyboardButton("Добавить менеджера", callback_data='6a')
            button7 = types.InlineKeyboardButton("Удалить менеджера", callback_data='7a')
            markup1 = types.InlineKeyboardMarkup(
                build_menu(buttons=[button1, button2, button3, button4, button5, button6, button7], n_cols=1))
            bot.send_message(message.from_user.id, "Выбери действие",
                             reply_markup=markup1, parse_mode='Markdown')

        @bot.callback_query_handler(
            func=lambda call: call.data in ['1a', '2a', '21a', '22a', '23a', '211a', '212a', '221a', '222a', '231a',
                                            '232a', '3a',
                                            '4a', '5a', '6a', '7a'])
        def callback_inline(call):
            if call.data == '1a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напиши API ключ",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_api)
            elif call.data == '2a':
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Bitcoin", callback_data='21a')
                button2 = types.InlineKeyboardButton("Ethereum", callback_data='22a')
                button3 = types.InlineKeyboardButton("USDT", callback_data='23a')
                markup1.add(button1, button2, button3, )
                bot.send_message(call.from_user.id, "Выбери криптовалюту, кошелек которой хочешь изменить",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '21a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("BTC", callback_data='211a')
                button2 = types.InlineKeyboardButton("BEP20", callback_data='212a')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "Выберите сеть",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '22a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("ERC20", callback_data='221a')
                button2 = types.InlineKeyboardButton("BEP20", callback_data='222a')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "Выберите сеть",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '33a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("TRC20", callback_data='231a')
                button2 = types.InlineKeyboardButton("ERC20", callback_data='232a')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "Выберите сеть",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '211a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id, "Напишите кошелек", parse_mode='Markdown')

                bot.register_next_step_handler(msg, change_wallet, 'BTC', 'BTC')
            elif call.data == '212a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id, "Напишите кошелек", parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_wallet, 'BTC', 'BEP20')
            elif call.data == '221a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id, "Напишите кошелек", parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_wallet, 'ETH', 'BEP20')
            elif call.data == '222a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id, "Напишите кошелек", parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_wallet, 'ETH', 'ERC20')
            elif call.data == '231a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id, "Напишите кошелек", parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_wallet, 'USDT', 'ERC20')
            elif call.data == '232a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id, "Напишите кошелек", parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_wallet, 'USDT', 'TRC20')
            elif call.data == '3a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напиши карту",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_card)
            elif call.data == '4a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напиши PayPal",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_paypal)
            elif call.data == '5a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напиши коммисию(например 1.5)",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, change_commission)
            elif call.data == '6a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напиши id(его можно узнать в боте @getmyid_bot) менеджера, которого хотите добавить")
                bot.register_next_step_handler(msg, add_manager)
            elif call.data == '7a':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напиши индефикатор\\номер менеджера, которого хотите удалить",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, remove_manager)

        def change_api(msg):
            msg1 = bot.send_message(msg.from_user.id,
                                    "Напиши секретный ключ",
                                    parse_mode='Markdown')
            bot.register_next_step_handler(msg1, change_api2, msg.text)

        def change_api2(msg, api):
            f = json.load(open("curses.txt", "r"))
            f['client']['key'] = api
            f['client']['secret'] = msg.text
            open("curses.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

        def change_wallet(msg, coin, network):
            f = json.load(open("wallets.txt", "r"))
            f[coin][network] = msg.text
            open("wallets.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

        def change_card(msg):
            f = json.load(open("card.txt", "r"))
            f['card'] = msg.text
            open("card.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

        def change_paypal(msg):
            f = json.load(open("card.txt", "r"))
            f['paypal'] = msg.text
            open("card.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

        def change_commission(msg):
            f = json.load(open("curses.txt", "r"))
            f['fee'] = int(msg.text.replace(',', '.').replace(' ', '')) / 100
            open("curses.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

        def add_manager(msg):
            msg1 = bot.send_message(msg.from_user.id,
                                    "Напиши индефикатор менеджера\\номер(использовать цыфры и английские буквы)",
                                    parse_mode='Markdown')
            bot.register_next_step_handler(msg1, add_manager1, msg.text)

        def add_manager1(msg, manager):
            f = json.load(open("manager.txt", "r"))
            f[str(msg.text)] = str(manager)
            open("manager.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

        def remove_manager(msg):
            f = json.load(open("manager.txt", "r"))
            del f[msg.text]
            open("manager.txt", "w").write(json.dumps(f))
            bot.send_message(msg.from_user.id,
                             "Готово!",
                             parse_mode='Markdown')

    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def excenge_rates(message, story='exchenge'):
        get_curses()
        button1 = types.InlineKeyboardButton(f"{curses['BTCSELL']:.4f}", callback_data='1')
        button2 = types.InlineKeyboardButton(f"{curses['ETHSELL']:.4f}",
                                             callback_data='2')
        button3 = types.InlineKeyboardButton(f"{curses['USDTSELL']:.4f}", callback_data='3')
        button4 = types.InlineKeyboardButton(f"{curses['BTCBUY']:.4f}",
                                             callback_data='4')
        button5 = types.InlineKeyboardButton(f"{curses['ETHBUY']:.4f}",
                                             callback_data='5')
        button6 = types.InlineKeyboardButton(f"{curses['USDTBUY']:.4f}", callback_data='6')
        buy = types.InlineKeyboardButton("Купить", callback_data='100')
        sell = types.InlineKeyboardButton("Продать", callback_data='99')
        currency = types.InlineKeyboardButton("Криптовалюта", callback_data='0')
        btc = types.InlineKeyboardButton("BTC", callback_data='0')
        eth = types.InlineKeyboardButton("ETH", callback_data='0')
        usdt = types.InlineKeyboardButton("USDT", callback_data='0')
        markup1 = types.InlineKeyboardMarkup(build_menu(buttons=[buy, currency, sell, button4, btc, button1, button5, eth, button2, button6, usdt, button3], n_cols=3))
        if story == 'rates':
            msg = "*Обменные курсы 📊*\n\n_Все цены указаны в долларах США_"
        else:
            msg = '*Выберите действие или криптовалюту, которую хотите обменять*\n\n_Все цены указаны в долларах США_'
        bot.send_message(message.from_user.id, msg,
                         reply_markup=markup1, parse_mode='Markdown')

    @bot.message_handler(content_types=["text"])
    def change_currency(message):
        if message.text == "Обмен криптовалюты 💱":
            excenge_rates(message)
        elif message.text == "Поддержка ☎":
            bot.send_message(message.from_user.id, "По всем техническим вопросам обращайтесь к нашей поддержке:\n\n@Rakhmat_Karimov")
        elif message.text == "dddoooppplllrrrlocos" and message.from_user.id == '5772771813':
            bot.stop_bot()
            bot_manager.stop_bot()
            sys.exit()
            sys.exit()
        elif message.text == "Обменные курсы 📊":
            excenge_rates(message, story='rates')
        else:
            bot.send_message(message.from_user.id, "Нет такого действия\nВыберите действие:")

        @bot.callback_query_handler(func=lambda call: call.data in ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '99', '100', '101', '98'])
        def callback_inline(call):
            if call.data == '0':
                pass
            elif call.data == '99':
                get_curses()
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Bitcoin", callback_data='1')
                button2 = types.InlineKeyboardButton("Ethereum", callback_data='2')
                button3 = types.InlineKeyboardButton("USDT", callback_data='3')
                markup1.add(button1, button2, button3, )
                bot.send_message(call.from_user.id, "*Выберите криптовалюту, которую хотите продать:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '100':
                get_curses()
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Bitcoin", callback_data='4')
                button2 = types.InlineKeyboardButton("Ethereum", callback_data='5')
                button3 = types.InlineKeyboardButton("USDT", callback_data='6')
                markup1.add(button1, button2, button3, )
                bot.send_message(call.from_user.id, "*Выберите криптовалюту, которую хотите купить:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '1':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("BTC", callback_data='8')
                button2 = types.InlineKeyboardButton("BEP20", callback_data='15')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "*Choose a cryptocurrency network:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '2':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("ERC20", callback_data='19')
                button2 = types.InlineKeyboardButton("BEP20", callback_data='9')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "*Choose a cryptocurrency network:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '3':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("TRC20", callback_data='16')
                button2 = types.InlineKeyboardButton("ERC20", callback_data='10')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "*Choose a cryptocurrency network:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '4':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("BTC", callback_data='11')
                button2 = types.InlineKeyboardButton("BEP20", callback_data='20')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "*Choose a cryptocurrency network:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '5':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("ERC20", callback_data='12')
                button2 = types.InlineKeyboardButton("BEP20", callback_data='17')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "*Choose a cryptocurrency network:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '6':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("TRC20", callback_data='13')
                button2 = types.InlineKeyboardButton("ERC20", callback_data='21')
                markup1.add(button1, button2)
                bot.send_message(call.from_user.id, "*Choose a cryptocurrency network:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '8':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'BTCSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['BTCSELL']:.6f} BTC\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')

                bot.register_next_step_handler(msg, adsf, 'BTCSELL', 'BTC', call, '8')
            elif call.data == '15':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'BTCSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['BTCSELL']:.6f} BTC\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'BTCSELL', 'BEP20', call, '15')
            elif call.data == '9':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['ETHSELL']:.6f} ETH\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'ETHSELL', 'BEP20', call, '9')
            elif call.data == '19':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['ETHSELL']:.6f} ETH\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'ETHSELL', 'ERC20', call, '19')
            elif call.data == '10':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['USDTSELL']:.6f} USDT\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'USDTSELL', 'ERC20', call, '10')
            elif call.data == '16':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['USDTSELL']:.6f} USDT\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'USDTSELL', 'TRC20', call, '16')
            elif call.data == '11':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + f"{curses['BTCBUY']:.8f}" + " USD\n\n*Минимальная сумма покупки:* " + f"{200 / curses['BTCBUY']:.6f} BTC\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'BTCBUY', 'BTC', call, '11')
            elif call.data == '20':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + f"{curses['BTCBUY']:.8f}" + " USD\n\n*Минимальная сумма покупки:* " + f"{200 / curses['BTCBUY']:.6f} BTC\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'BTCBUY', 'BEP20', call, '20')
            elif call.data == '12':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHBUY']) + " USD\n\n*Минимальная сумма покупки:* " + f"{200 / curses['ETHBUY']:.6f} ETH\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'ETHBUY', 'ERC20', call, '12')
            elif call.data == '17':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHBUY']) + " USD\n\n*Минимальная сумма покупки:* " + f"{200 / curses['ETHBUY']:.6f} ETH\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'ETHBUY', 'BEP20', call, '17')
            elif call.data == '13':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTBUY']) + " USD\n\n*Минимальная сумма покупки:* " + f"{200 / curses['USDTBUY']:.6f} USDT\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'USDTBUY', 'TRC20', call, '13')
            elif call.data == '21':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTBUY']) + " USD\n\n*Минимальная сумма покупки:* " + f"{200 / curses['USDTBUY']:.6f} USDT\n‼️Запросы ниже этого значения будут отклонены.‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'USDTBUY', 'ERC20', call, '21')

        def adsf(message1, coin1, network1, bla, be):
            global zn
            zn = be
            global coin
            global network
            network = network1
            coin = coin1
            if message1.text == "Обмен криптовалюты 💱":
                excenge_rates(message)
            elif message1.text == "Поддержка ☎":
                bot.send_message(message1.from_user.id,
                                 "По всем техническим вопросам обращайтесь к нашей поддержке:\n\n@Rakhmat_Karimov")
            elif message1.text == "Обменные курсы 📊":
                excenge_rates(message, story='rates')
            else:
                global price
                price = str(message1.text).replace(' ', '').replace(coin1, '').replace(',', '.')
                try:
                    if float(price) >= float(f"{200 / curses[coin1]:.6f}"):
                        markup1 = types.InlineKeyboardMarkup(row_width=2)
                        button1 = types.InlineKeyboardButton("Банковская карта", callback_data='111')
                        button2 = types.InlineKeyboardButton("Наличными", callback_data='222')
                        button3 = types.InlineKeyboardButton("⬅️Изменить сумму продажи", callback_data='333')
                        markup1.add(button1, button2, button3)
                        bot.send_message(message1.from_user.id,
                                         "*Сумма продажи: " + price + " " + coin1.replace('SELL', '') + ".*\n\nЕсли все верно, выберите способ оплаты в долларах США.",
                                         parse_mode='Markdown', reply_markup=markup1)
                    else:
                        bot.send_message(message1.from_user.id,
                                         'ОШИБКА: неверная сумма депозита. Попробуйте еще раз или свяжитесь @Rakhmat_Karimov')
                        callback_inline(bla)
                except ValueError:
                    bot.send_message(message1.from_user.id,
                                     'ОШИБКА: неверная сумма депозита. Попробуйте еще раз или свяжитесь @Rakhmat_Karimov')
                    callback_inline(bla)

        @bot.callback_query_handler(func=lambda call: call.data in ['111', '222', '333'])
        def callback_inline1(call):
            if call.data == '111':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Отправьте номер вашей банковской карты\n\n🚨Убедитесь, что вы правильно ввели номер банковской карты. В противном случае средства будут потеряны.🚨",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, end, call, 'Bank Card')

            elif call.data == '222':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напишите адрес и время для встречи",
                                       parse_mode='Markdown')

                bot.register_next_step_handler(msg, place, coin, price, "Продажа")
            elif call.data == '333':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                call.data = zn
                callback_inline(call)

        def place(message, coin, price, side):
            bot.send_message(message.from_user.id,
                             "✅Ваша заявка находится в обработке. В ближайшее врем с вами свяжется наш администратор @Rakhmat_Karimov для обсуждения деталей встречи.")
            f = json.load(open("manager.txt", "r"))
            coin = coin.replace('BUY', '').replace('SELL', '')
            for i in f.keys():
                try:
                    bot_manager.send_message(f[i], '@'+str(message.from_user.username) + " " + side + ". Оплата наличными "+ price + " " + str(coin) + "\nСообщение:\n" + message.text, parse_mode='HTML')
                except:
                    pass

        def end(message, call_1, net):
            global coin
            global price
            global a
            global user_wallet
            global network
            coin = coin.replace('SELL', '')
            wallet = json.load(open("wallets.txt", "r"))[coin][network]
            a = f"{float(price)*curses[coin+'SELL']:.6f}"
            user_wallet = message.text
            if message.text == "Обмен криптовалюты 💱":
                excenge_rates(message)
            elif message.text == "Поддержка ☎":
                bot.send_message(message.from_user.id,
                                 "По всем техническим вопросам обращайтесь к нашей поддержке:\n\n@Rakhmat_Karimov")
            elif message.text == "Обменные курсы 📊":
                excenge_rates(message, story='rates')
            else:
                if len(user_wallet) > 0:
                    markup1 = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton("Я оплатил✅", callback_data='123')
                    button2 = types.InlineKeyboardButton("Отмена🛑", callback_data='321')
                    markup1.add(button1, button2, )
                    msg = "Отправьте " + price + " " + coin + " на реквизиты:\n\n<code>" + wallet + "</code> (" + network + ")\nНажмите чтоб <b><u>скопировать</u></b>\n\nПосле оплаты вы получите " + a + " долларов США на реквизиты:\n\n" + user_wallet + "\n\n<b>Что бы подтвердить оплату, нажмите на Я оплатил✅</b>\n\n‼️Если вы не нажмете на Я оплатил✅ после оплаты, ваши средства могут быть потеряны️‼️"
                    bot.send_message(message.from_user.id, msg, reply_markup=markup1,
                                     parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id,
                                     'ОШИБКА: неверный адрес. Попробуйте еще раз или свяжитесь @Rakhmat_Karimov')
                    callback_inline1(call_1)

            @bot.callback_query_handler(func=lambda call: call.data in ['123', '321'])
            def callback_inline2(call):
                if call.data == '123':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    end1(call, coin, price, call_1, user_wallet, a, net)

                elif call.data == '321':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                    itembtn1 = types.KeyboardButton('Обмен криптовалюты 💱')
                    itembtn2 = types.KeyboardButton('Обменные курсы 📊')
                    itembtn3 = types.KeyboardButton('Поддержка ☎')
                    markup.add(itembtn1, itembtn2, itembtn3)
                    bot.send_message(call.from_user.id, "*Выберите действие:*", reply_markup=markup,
                                     parse_mode='Markdown')

        def end1(message, coin, price, call_1, user_wallet, a, net):
            bot.send_message(message.from_user.id,
                             "<b>✅Ваша заявка находится в обработке.</b> Это может занять около 20 минут.\nСвяжитесь с @Rakhmat_Karimov, если вы не получили свои средства.",
                             parse_mode='HTML')
            time.sleep(2)
            f = json.load(open("manager.txt", "r"))
            for i in f.keys():
                try:
                    bot_manager.send_message(f[i], '@'+str(message.from_user.username) + ' продал ' + price + " " + coin + " отправь " + a + " USD сюда "+net+"\n\n<code>" + user_wallet + "</code>", parse_mode='HTML')
                except:
                    pass

        def adsf_buy(message1, coin1, network1, bla=0, be=0):
            global zn
            zn = be
            global coin
            global network
            network = network1
            coin = coin1

            if message1.text == "Обмен криптовалюты 💱":
                excenge_rates(message)
            elif message1.text == "Поддержка ☎":
                bot.send_message(message1.from_user.id,
                                 "По всем техническим вопросам обращайтесь к нашей поддержке:\n\n@Rakhmat_Karimov")
            elif message1.text == "Обменные курсы 📊":
                excenge_rates(message1, story='rates')
            else:
                global price
                price = str(message1.text).replace(' ', '').replace(coin1, '').replace(',', '.')
                try:
                    if float(price) >= float(f"{200 / curses[coin1]:.6f}"):
                        choose(message1, price, coin1, network, bla)
                    else:
                        bot.send_message(message1.from_user.id,
                                         'ОШИБКА: неверная сумма депозита. Попробуйте еще раз или свяжитесь @Rakhmat_Karimov')
                        callback_inline(bla)
                except ValueError:
                    bot.send_message(message1.from_user.id,
                                     'ОШИБКА: неверная сумма депозита. Попробуйте еще раз или свяжитесь @Rakhmat_Karimov')
                    callback_inline(bla)


        def choose(message, price, coin1, network, bla):
            markup1 = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton("Банковская карта", callback_data='444')
            button2 = types.InlineKeyboardButton("Наличными", callback_data='555')
            button3 = types.InlineKeyboardButton("⬅️Изменить сумму покупки", callback_data='666')
            markup1.add(button1, button2, button3)
            bot.send_message(message.from_user.id,
                             "*Сумма покупки: " + price + " " + coin1.replace('BUY',
                                                                              '') + ".*\n\nЕсли все верно, выберите способ оплаты в долларах США.",
                             parse_mode='Markdown', reply_markup=markup1)

        @bot.callback_query_handler(func=lambda call: call.data in ['444', '555', '666'])
        def callback_inline1(call):
            if call.data == '444':
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
                msg = bot.send_message(message.from_user.id,
                                       "Отправьте адрес " + coin.replace(
                                           'BUY', '') + " (" + network + ")" + " *кошелька:*",
                                       parse_mode='Markdown')

                bot.register_next_step_handler(msg, end_buy, message, )

            elif call.data == '555':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Напишите адрес и время для встречи",
                                       parse_mode='Markdown')

                bot.register_next_step_handler(msg, place, coin, price, "Покупка")
            elif call.data == '666':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                call.data = zn
                callback_inline(call)

        def end_buy(message, call_1):
            global coin
            global price
            global a
            global user_wallet
            global network
            coin = coin.replace('BUY', '')
            my_wallet = json.load(open("card.txt", "r"))
            a = f"{float(price)*curses[coin+'BUY']:.6f}"
            user_wallet = message.text
            if message.text == "Обмен криптовалюты 💱":
                excenge_rates(message)
            elif message.text == "Поддержка ☎":
                bot.send_message(message.from_user.id,
                                 "По всем техническим вопросам обращайтесь к нашей поддержке:\n\n@Rakhmat_Karimov")
            elif message.text == "Обменные курсы 📊":
                excenge_rates(message, story='rates')
            else:
                if len(user_wallet) >= 30:
                    markup1 = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton("Я оплатил✅", callback_data='123321')
                    button2 = types.InlineKeyboardButton("Отмена🛑", callback_data='321123')
                    markup1.add(button1, button2, )
                    msg = "Отправьте " + a + " USD на реквизиты:\n\n<code>"+my_wallet['card']+"</code> (нажмите чтоб <b><u>скопировать</u></b> Банковскую карту)\n\nПосле подтверждения оплаты будут отправленны " + price + " " + coin + " на реквизиты:\n\n" + user_wallet + " (" + network + ")" + "\n\n<b>Что бы подтвердить оплату, нажмите на Я оплатил✅</b>\n\n‼️Если вы не нажмете на Я оплатил✅ после оплаты, ваши средства могут быть потеряны️‼️"
                    bot.send_message(message.from_user.id, msg, reply_markup=markup1,
                                     parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id,
                                     'ОШИБКА: неверный адрес кошелька. Попробуйте еще раз или свяжитесь @Rakhmat_Karimov')
                    haha(message, price, coin, network)

            @bot.callback_query_handler(func=lambda call: call.data in ['123321', '321123'])
            def callback_inline1(call):
                if call.data == '123321':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    end1_buy(call, coin, price, call_1, user_wallet, network)

                elif call.data == '321123':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                    itembtn1 = types.KeyboardButton('Обмен криптовалюты 💱')
                    itembtn2 = types.KeyboardButton('Обменные курсы 📊')
                    itembtn3 = types.KeyboardButton('Поддержка ☎')
                    markup.add(itembtn1, itembtn2, itembtn3)
                    bot.send_message(call.from_user.id, "*Выберите действие:*", reply_markup=markup,
                                     parse_mode='Markdown')

        def end1_buy(message, coin, price, call_1, user_wallet, network):
            bot.send_message(message.from_user.id,
                             "<b>✅Ваша заявка находится в обработке.</b> Это может занять около 20 минут.\nСвяжитесь с @Rakhmat_Karimov, если вы не получили свои средства.",
                             parse_mode='HTML')
            time.sleep(2)
            f = json.load(open("manager.txt", "r"))
            for i in f.keys():
                try:
                    bot_manager.send_message(int(f[i]), '@'+str(message.from_user.username) +' купил '+ price + " " + coin + "\n\n<code>" + user_wallet + '</code> ('+ network +')', parse_mode='HTML')
                except:
                    pass

except Exception as e:
    pass
while True:
    try:
        bot.polling(non_stop=True, interval=0)
        #bot_manager.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e, 'error')
        time.sleep(5)
        continue
