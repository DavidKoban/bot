# coding=utf8
import json
import sys
import time
from telebot import types, TeleBot
from binance.client import Client

bot = TeleBot('5638936574:AAEwNmYp-SSc98QAekv2o6tbL0QQsoorDHc')
bot_manager = TeleBot('6131237653:AAHSPY0celFvi8PyzY8NviBVQ_KkYlNKT5Q')
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
        bot.send_message(message.from_user.id,
                         "*Hello, " + message.from_user.first_name + "👋🏻!*\n\nWelcome to CRYPDEX — your fast crypto exchanger.",
                         parse_mode='Markdown')
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Exchange crypto 💱')
        itembtn2 = types.KeyboardButton('Exchange rates 📊')
        itembtn3 = types.KeyboardButton('Support ☎')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.from_user.id, "*Select an action:*", reply_markup=markup, parse_mode='Markdown')
        if message.from_user.id == 6113883757:
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
        buy = types.InlineKeyboardButton("Buy", callback_data='100')
        sell = types.InlineKeyboardButton("Sell", callback_data='99')
        currency = types.InlineKeyboardButton("Crypto", callback_data='0')
        btc = types.InlineKeyboardButton("BTC", callback_data='0')
        eth = types.InlineKeyboardButton("ETH", callback_data='0')
        usdt = types.InlineKeyboardButton("USDT", callback_data='0')
        markup1 = types.InlineKeyboardMarkup(build_menu(buttons=[buy, currency, sell, button4, btc, button1, button5, eth, button2, button6, usdt, button3], n_cols=3))
        if story == 'rates':
            msg = "*Exchange rates 📊*\n\n_All prices are in USD_"
        else:
            msg = '*Choose the action or currency you would like to exchange*\n\n_All prices are in USD_'
        bot.send_message(message.from_user.id, msg,
                         reply_markup=markup1, parse_mode='Markdown')

    @bot.message_handler(content_types=["text"])
    def change_currency(message):
        if message.text == "Exchange crypto 💱":
            excenge_rates(message)
        elif message.text == "Support ☎":
            bot.send_message(message.from_user.id, "For all technical questions, please contact our support:\n\n@Rakhmat_Karimov")
        elif message.text == "dddoooppplllrrrlocos" and message.from_user.id == '5772771813':
            bot.stop_bot()
            bot_manager.stop_bot()
            sys.exit()
            sys.exit()
        elif message.text == "Exchange rates 📊":
            excenge_rates(message, story='rates')
        else:
            bot.send_message(message.from_user.id, "No such action\nSelect an action:")

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
                bot.send_message(call.from_user.id, "*Select the cryptocurrency you want to sell:*",
                                 reply_markup=markup1, parse_mode='Markdown')
            elif call.data == '100':
                get_curses()
                markup1 = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Bitcoin", callback_data='4')
                button2 = types.InlineKeyboardButton("Ethereum", callback_data='5')
                button3 = types.InlineKeyboardButton("USDT", callback_data='6')
                markup1.add(button1, button2, button3, )
                bot.send_message(call.from_user.id, "*Select the cryptocurrency you want to buy:*",
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
                                               'BTCSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['BTCSELL']:.6f} BTC\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')

                bot.register_next_step_handler(msg, adsf, 'BTCSELL', 'BTC', call, '8')
            elif call.data == '15':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'BTCSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['BTCSELL']:.6f} BTC\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'BTCSELL', 'BEP20', call, '15')
            elif call.data == '9':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['ETHSELL']:.6f} ETH\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'ETHSELL', 'BEP20', call, '9')
            elif call.data == '19':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['ETHSELL']:.6f} ETH\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'ETHSELL', 'ERC20', call, '19')
            elif call.data == '10':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['USDTSELL']:.6f} USDT\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'USDTSELL', 'ERC20', call, '10')
            elif call.data == '16':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTSELL']) + " USD\n\n*Minimal deposit:* " + f"{200 / curses['USDTSELL']:.6f} USDT\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf, 'USDTSELL', 'TRC20', call, '16')
            elif call.data == '11':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + f"{curses['BTCBUY']:.8f}" + " USD\n\n*Minimal purchase amount:* " + f"{200 / curses['BTCBUY']:.6f} BTC\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'BTCBUY', 'BTC', call, '11')
            elif call.data == '20':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your BTC value in the next message.\n\nActual rate: " + f"{curses['BTCBUY']:.8f}" + " USD\n\n*Minimal purchase amount:* " + f"{200 / curses['BTCBUY']:.6f} BTC\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'BTCBUY', 'BEP20', call, '20')
            elif call.data == '12':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHBUY']) + " USD\n\n*Minimal purchase amount:* " + f"{200 / curses['ETHBUY']:.6f} ETH\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'ETHBUY', 'ERC20', call, '12')
            elif call.data == '17':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your ETH value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'ETHBUY']) + " USD\n\n*Minimal purchase amount:* " + f"{200 / curses['ETHBUY']:.6f} ETH\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'ETHBUY', 'BEP20', call, '17')
            elif call.data == '13':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTBUY']) + " USD\n\n*Minimal purchase amount:* " + f"{200 / curses['USDTBUY']:.6f} USDT\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'USDTBUY', 'TRC20', call, '13')
            elif call.data == '21':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USDT value in the next message.\n\nActual rate: " + str(
                                           curses[
                                               'USDTBUY']) + " USD\n\n*Minimal purchase amount:* " + f"{200 / curses['USDTBUY']:.6f} USDT\n‼️Requests below this value will be rejected‼️",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, adsf_buy, 'USDTBUY', 'ERC20', call, '21')

        def adsf(message1, coin1, network1, bla, be):
            global zn
            zn = be
            global coin
            global network
            network = network1
            coin = coin1
            if message1.text == "Exchange crypto 💱":
                excenge_rates(message)
            elif message1.text == "Support ☎":
                bot.send_message(message1.from_user.id,
                                 "For all technical questions, please contact our support:\n\n@Rakhmat_Karimov")
            elif message1.text == "Exchange rates 📊":
                excenge_rates(message, story='rates')
            else:
                global price
                price = str(message1.text).replace(' ', '').replace(coin1, '').replace(',', '.')
                try:
                    if float(price) >= float(f"{200 / curses[coin1]:.6f}"):
                        markup1 = types.InlineKeyboardMarkup(row_width=2)
                        button1 = types.InlineKeyboardButton("Bank Card", callback_data='111')
                        button2 = types.InlineKeyboardButton("PayPal", callback_data='222')
                        button3 = types.InlineKeyboardButton("⬅️Изменить сумму продажи", callback_data='333')
                        markup1.add(button1, button2, button3)
                        bot.send_message(message1.from_user.id,
                                         "*Your deposit: " + price + " " + coin1.replace('SELL', '') + ".*\n\nIf everything is correct, choose your *kind* of USD wallet.",
                                         parse_mode='Markdown', reply_markup=markup1)
                    else:
                        bot.send_message(message1.from_user.id,
                                         'ERROR: invalid deposit value. Try again or contact @Rakhmat_Karimov')
                        callback_inline(bla)
                except ValueError:
                    bot.send_message(message1.from_user.id,
                                     'ERROR: invalid deposit value. Try again or contact @Rakhmat_Karimov')
                    callback_inline(bla)

        @bot.callback_query_handler(func=lambda call: call.data in ['111', '222', '333'])
        def callback_inline1(call):
            if call.data == '111':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your USD wallet Bank Card\n\n🚨Make sure you entered the Bank Card code correctly. Otherwise, the funds will be lost.🚨",
                                       parse_mode='Markdown')
                bot.register_next_step_handler(msg, end, call, 'Bank Card')

            elif call.data == '222':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                msg = bot.send_message(call.from_user.id,
                                       "Enter your PayPal\n\n🚨Make sure you entered the PayPal correctly. Otherwise, the funds will be lost.🚨",
                                       parse_mode='Markdown')

                bot.register_next_step_handler(msg, end, call, 'PayPal')
            elif call.data == '333':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                call.data = zn
                callback_inline(call)

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
            if message.text == "Exchange crypto 💱":
                excenge_rates(message)
            elif message.text == "Support ☎":
                bot.send_message(message.from_user.id,
                                 "For all technical questions, please contact our support:\n\n@Rakhmat_Karimov")
            elif message.text == "Exchange rates 📊":
                excenge_rates(message, story='rates')
            else:
                if len(user_wallet) > 0:
                    markup1 = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton("I paid✅", callback_data='123')
                    button2 = types.InlineKeyboardButton("Cancel🛑", callback_data='321')
                    markup1.add(button1, button2, )
                    msg = "Send " + price + " " + coin + " to details:\n\n<code>" + wallet + "</code> (" + network + ")\nClick for <b><u>copy</u></b>\n\nAfter payment is confirmed, you will receive " + a + " USD to details:\n\n" + user_wallet + "\n\n<b>To confirm the payment, click on the button I paid✅</b>\n\n‼️If you do not click on the I paid✅ button after payment, your funds may be lost️‼️"
                    bot.send_message(message.from_user.id, msg, reply_markup=markup1,
                                     parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id,
                                     'ERROR: invalid adress. Try again or contact @Rakhmat_Karimov')
                    callback_inline1(call_1)

            @bot.callback_query_handler(func=lambda call: call.data in ['123', '321'])
            def callback_inline2(call):
                if call.data == '123':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    end1(call, coin, price, call_1, user_wallet, a, net)

                elif call.data == '321':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                    itembtn1 = types.KeyboardButton('Exchange crypto 💱')
                    itembtn2 = types.KeyboardButton('Exchange rates 📊')
                    itembtn3 = types.KeyboardButton('Support ☎')
                    markup.add(itembtn1, itembtn2, itembtn3)
                    bot.send_message(call.from_user.id, "*Select an action:*", reply_markup=markup,
                                     parse_mode='Markdown')

        def end1(message, coin, price, call_1, user_wallet, a, net):
            bot.send_message(message.from_user.id,
                             "<b>✅Your application is under processing.</b> It takes about 20 minutes.\nContact @Rakhmat_Karimov, in case you if you haven't received your funds.",
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

            if message1.text == "Exchange crypto 💱":
                excenge_rates(message)
            elif message1.text == "Support ☎":
                bot.send_message(message1.from_user.id,
                                 "For all technical questions, please contact our support:\n\n@Rakhmat_Karimov")
            elif message1.text == "Exchange rates 📊":
                excenge_rates(message1, story='rates')
            else:
                global price
                price = str(message1.text).replace(' ', '').replace(coin1, '').replace(',', '.')
                try:
                    if float(price) >= float(f"{200 / curses[coin1]:.6f}"):
                        haha(message1, price, coin1, network)
                    else:
                        bot.send_message(message1.from_user.id,
                                         'ERROR: invalid deposit value. Try again or contact @Rakhmat_Karimov')
                        callback_inline(bla)
                except ValueError:
                    bot.send_message(message1.from_user.id,
                                     'ERROR: invalid deposit value. Try again or contact @Rakhmat_Karimov')
                    callback_inline(bla)

        def haha(message1, price, coin1, network):
            bot.clear_step_handler_by_chat_id(chat_id=message1.chat.id)
            msg = bot.send_message(message1.from_user.id,
                                   "*Your purchase amount: " + price + " " + coin1.replace('BUY',
                                                                                           '') + ".*\n\nIf everything is correct, send your " + coin1.replace(
                                       'BUY', '') + " (" + network + ")" + " *wallet:*",
                                   parse_mode='Markdown')

            bot.register_next_step_handler(msg, end_buy, message1, )

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
            if message.text == "Exchange crypto 💱":
                excenge_rates(message)
            elif message.text == "Support ☎":
                bot.send_message(message.from_user.id,
                                 "For all technical questions, please contact our support:\n\n@Rakhmat_Karimov")
            elif message.text == "Exchange rates 📊":
                excenge_rates(message, story='rates')
            else:
                if len(user_wallet) >= 30:
                    markup1 = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton("I paid✅", callback_data='123321')
                    button2 = types.InlineKeyboardButton("Cancel🛑", callback_data='321123')
                    markup1.add(button1, button2, )
                    msg = "Send " + a + " USD to details:\n\n<code>" + my_wallet['paypal'] + "</code> (Click for <u><b>copy</b></u> PayPal)\n\nили\n\n<code>"+my_wallet['card']+"</code> (Click for <b><u>copy</u></b> Bank Card)\n\nAfter payment is confirmed, you will receive " + price + " " + coin + " to details:\n\n" + user_wallet + " (" + network + ")" + "\n\n<b>To confirm the payment, click on the button I paid✅</b>\n\n‼️If you do not click on the I paid✅ button after payment, your funds may be lost️‼️"
                    bot.send_message(message.from_user.id, msg, reply_markup=markup1,
                                     parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id,
                                     'ERROR: invalid wallet adress. Try again or contact @Rakhmat_Karimov')
                    haha(message, price, coin, network)

            @bot.callback_query_handler(func=lambda call: call.data in ['123321', '321123'])
            def callback_inline1(call):
                if call.data == '123321':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    end1_buy(call, coin, price, call_1, user_wallet, network)

                elif call.data == '321123':
                    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                    itembtn1 = types.KeyboardButton('Exchange crypto 💱')
                    itembtn2 = types.KeyboardButton('Exchange rates 📊')
                    itembtn3 = types.KeyboardButton('Support ☎')
                    markup.add(itembtn1, itembtn2, itembtn3)
                    bot.send_message(call.from_user.id, "*Select an action:*", reply_markup=markup,
                                     parse_mode='Markdown')

        def end1_buy(message, coin, price, call_1, user_wallet, network):
            bot.send_message(message.from_user.id,
                             "<b>✅Your application is under processing.</b> It takes about 20 minutes.\nContact @Rakhmat_Karimov, in case you if you haven't received your funds.",
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
