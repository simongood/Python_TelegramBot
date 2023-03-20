from telegram.ext import Filters, Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import random

updater = Updater(token='xxxxxxxx', use_context=True)
dispatcher = updater.dispatcher

# 開牌 ， 洗牌
card = [i+1 for i in range(52)]  # 整副新牌(1~13 = 梅花， 14~26 = 方塊， 27~39 = 愛心， 40~52 = 黑桃)
random.shuffle(card)  # 洗牌
cnt = 7     # 抽牌計數(抽第幾張，美抽一張加一)
    # 翻譯牌組
card2 = [0] * 52 # (翻譯牌組)
r = 0
while r < 52:
    if 1 <= card[r] < 14:
        card2[r] = "♣" + str(card[r])
    elif 14 <= card[r] < 27:
        card2[r] = "♦" + str(card[r]-13)
    elif 27 <= card[r] < 40:
        card2[r] = "❤" + str(card[r]-26)
    else:
        card2[r] = "♠" + str(card[r]-39)
    r += 1


# 設定開頭，結尾
rows_head = ["♣(0):", "♦(1):", "❤(2):", "♠(3):", "🂠(4):",] + [f"row{i}({i+5}):" for i in range(7)]
rows_tail = [
        [], [], [], [], [], [card2[0]], [card2[1], " *"], [card2[2], " *", " *"],\
        [card2[3], " *", " *", " *"], [card2[4], " *", " *", " *", " *"],\
        [card2[5], " *", " *", " *", " *", " *"], [card2[6], " *", " *", " *", " *", " *", " *"]
    ]
    # 翻譯牌組
rows_tail2 = [""]*12
for i in range(12):
    rows_tail2[i] = "".join(rows_tail[i])

# 開始盤面方程式

def init(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,\
        text="\n".join([head + tail2 for head , tail2 in zip(rows_head, rows_tail2)])
    )
    # 互動按鈕
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='重玩or發牌紐', reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('重玩', callback_data='a'),
            InlineKeyboardButton('發牌', callback_data='b')]])
    )

# 開牌重製方程式
K = 0
def func(update, context):
    global cnt, K
    global rows_tail, card2, rows_tail2, rows_head
    if update.callback_query.data == 'a':
        # 開牌 ， 洗牌
        card = [i + 1 for i in range(52)]  # 整副新牌(1~13 = 梅花， 14~26 = 方塊， 27~39 = 愛心， 40~52 = 黑桃)
        random.shuffle(card)  # 洗牌
        cnt = 7  # 抽牌計數(抽第幾張，美抽一張加一)
        # 翻譯牌組
        card2 = [0] * 52  # (翻譯牌組)
        r = 0
        while r < 52:
            if 1 <= card[r] < 14:
                card2[r] = "♣" + str(card[r])
            elif 14 <= card[r] < 27:
                card2[r] = "♦" + str(card[r] - 13)
            elif 27 <= card[r] < 40:
                card2[r] = "❤" + str(card[r] - 26)
            else:
                card2[r] = "♠" + str(card[r] - 39)
            r += 1

        # 設定開頭，結尾
        rows_head = ["♣(0):", "♦(1):", "❤(2):", "♠(3):", "🂠(4):", ] + [f"row{i}({i + 5}):" for i in range(7)]
        rows_tail = [
            [], [], [], [], [], [card2[0]], [card2[1], " *"], [card2[2], " *", " *"],\
            [card2[3], " *", " *", " *"], [card2[4], " *", " *", " *", " *"],\
            [card2[5], " *", " *", " *", " *", " *"], [card2[6], " *", " *", " *", " *", " *", " *"]
        ]
        # 翻譯牌組
        rows_tail2 = [""] * 12
        for i in range(12):
            rows_tail2[i] = "".join(rows_tail[i])
        context.bot.edit_message_text("\n".join([head + tail2 for head , tail2 in zip(rows_head, rows_tail2)]),
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)
        # 互動按鈕
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='重玩or發牌紐', reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('重玩', callback_data='a'),
                InlineKeyboardButton('發牌', callback_data='b')]])
        )
    else:
        if K < 25:
            rows_tail[4].append(card2[cnt])
            rows_tail[4].insert(0, rows_tail[4].pop())
            cnt += 1
            K += 1
            for i in range(12):
                rows_tail2[i] = "".join(rows_tail[i])
            context.bot.edit_message_text("\n".join([head + tail2 for head, tail2 in zip(rows_head, rows_tail2)]),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id)
            context.bot.send_message(               # 互動按鈕
                chat_id=update.effective_chat.id, text='重玩or發牌紐', reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('重玩', callback_data='a'),
                    InlineKeyboardButton('發牌', callback_data='b')]])
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='你已無牌可翻')
# 移動盤面方程式
def move(update, context):
    # 要求輸入的格式
    context.bot.send_message(
        chat_id=update.effective_chat.id,\
        text='請輸入格式 "6 0 1" 數字 :\n將畫面上第 6 列（暫存區第一列）的第 0 張牌（最上面那張）移動至畫面上第 1 列(♦的答案區)')

    # 偵測移動想法並移動
    def repeat(update, context):
        global cnt
        pos = list(map(int, update.message.text.split()))

    # 檢查第一個數
        if pos[0] == 4 and pos[1] > 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='開牌區只可移動第0張牌')
        elif 12 <= pos[0]:          # 第一個樹錯誤
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='不可選取無牌地方移動')
        else:   # 第一個數正確
    # 檢查第二個數
            if pos[1] >= len(rows_tail[pos[0]]):     # 第二個數錯誤
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text='不可選取無牌地方移動')
            elif rows_tail[pos[0]][pos[1]] == " *":
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text='不可選取未翻開的牌移動')
            else:  # 第二個數正確
    #檢查第三個數
                if pos[2] == 4:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, text='不可將牌移至翻牌區')
                elif len(rows_tail[pos[2]]) == 0:
    # 執行移動
                    for i in range(pos[1] + 1):
                        rows_tail[pos[2]].append(rows_tail[pos[0]][pos[1] - i])
                        rows_tail[pos[2]].insert(0, rows_tail[pos[2]].pop())
                    for i in range(pos[1] + 1):
                        rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                    if len(rows_tail[pos[0]]) > 0 and rows_tail[pos[0]][0] == ' *':  # 若遇到*在地0張則抽一張牌替代*
                        rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                        rows_tail[pos[0]].append(card2[cnt])
                        rows_tail[pos[0]].insert(0, rows_tail[pos[0]].pop())
                        cnt += 1
                    for i in range(12):
                        rows_tail2[i] = "".join(rows_tail[i])
                    context.bot.send_message(
                        chat_id=update.effective_chat.id, \
                        text="\n".join([head + tail2 for head, tail2 in zip(rows_head, rows_tail2)])
                    )
                elif rows_tail[pos[0]][pos[1]][-2:-1] in ['♣', '♦', '❤', '♠']:  # 0~9的牌
                    if rows_tail[pos[0]][pos[1]][-1:] == '9' and rows_tail[pos[2]][0][-2:] == '10':
    # 執行移動
                        for i in range(pos[1] + 1):
                            rows_tail[pos[2]].append(rows_tail[pos[0]][pos[1] - i])
                            rows_tail[pos[2]].insert(0, rows_tail[pos[2]].pop())
                        for i in range(pos[1] + 1):
                            rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                        if len(rows_tail[pos[0]]) > 0 and rows_tail[pos[0]][0] == ' *':  # 若遇到*在地0張則抽一張牌替代*
                            rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                            rows_tail[pos[0]].append(card2[cnt])
                            rows_tail[pos[0]].insert(0, rows_tail[pos[0]].pop())
                            cnt += 1
                        for i in range(12):
                            rows_tail2[i] = "".join(rows_tail[i])
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,\
                            text="\n".join([head + tail2 for head, tail2 in zip(rows_head, rows_tail2)])
                        )
                    elif int(rows_tail[pos[2]][0][-1:]) - int(rows_tail[pos[0]][pos[1]][-1:]) == 1: # 原本在地0張位置的牌 - 移動過來的牌
    # 執行移動
                        for i in range(pos[1] + 1):
                            rows_tail[pos[2]].append(rows_tail[pos[0]][pos[1] - i])
                            rows_tail[pos[2]].insert(0, rows_tail[pos[2]].pop())
                        for i in range(pos[1] + 1):
                            rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                        if len(rows_tail[pos[0]]) > 0 and rows_tail[pos[0]][0] == ' *':  # 若遇到*在地0張則抽一張牌替代*
                            rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                            rows_tail[pos[0]].append(card2[cnt])
                            rows_tail[pos[0]].insert(0, rows_tail[pos[0]].pop())
                            cnt += 1
                        for i in range(12):
                            rows_tail2[i] = "".join(rows_tail[i])
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,\
                            text="\n".join([head + tail2 for head, tail2 in zip(rows_head, rows_tail2)])
                        )
                    else:
                        context.bot.send_message(
                            chat_id=update.effective_chat.id, text='只可移動至比前一張小並連續的牌')
                else:                                                          # 10~13的牌
                    if rows_tail[pos[2]][0][-2:-1] in ['♣', '♦', '❤', '♠']: # 若前一數為0~9
                        context.bot.send_message(
                            chat_id=update.effective_chat.id, text='只可移動至比前一張小並連續的牌')
                    elif int(rows_tail[pos[2]][0][-2:]) - int(rows_tail[pos[0]][pos[1]][-2:]) == 1:
    # 執行移動
                        for i in range(pos[1] + 1):
                            rows_tail[pos[2]].append(rows_tail[pos[0]][pos[1] - i])
                            rows_tail[pos[2]].insert(0, rows_tail[pos[2]].pop())
                        for i in range(pos[1] + 1):
                            rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                        if len(rows_tail[pos[0]]) > 0 and rows_tail[pos[0]][0] == ' *':  # 若遇到*在地0張則抽一張牌替代*
                            rows_tail[pos[0]].remove(rows_tail[pos[0]][0])
                            rows_tail[pos[0]].append(card2[cnt])
                            rows_tail[pos[0]].insert(0, rows_tail[pos[0]].pop())
                            cnt += 1
                        for i in range(12):
                            rows_tail2[i] = "".join(rows_tail[i])
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,\
                            text="\n".join([head + tail2 for head, tail2 in zip(rows_head, rows_tail2)])
                        )
                    else:
                        context.bot.send_message(
                            chat_id=update.effective_chat.id, text='只可移動至比前一張小並連續的牌')
        # 檢查遊戲是否成功
        if len(rows_tail[0]) == 13 and len(rows_tail[1]) == 13 and len(rows_tail[2]) == 13 and len(rows_tail[3]) == 13:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='你成功了！')
            # 互動按鈕
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='重玩or發牌紐', reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('再玩一次 ??', callback_data='a')]])
            )
        else:
            # 互動按鈕
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='重玩or發牌紐', reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('重玩', callback_data='a'),
                    InlineKeyboardButton('發牌', callback_data='b')]])
            )

    repeat_handler = MessageHandler(Filters.text & (~Filters.command), repeat)
    dispatcher.add_handler(repeat_handler)



dispatcher.add_handler(CallbackQueryHandler(func))

start_handler = CommandHandler('start', init)
dispatcher.add_handler(start_handler)


move_handler = CommandHandler('move', move)
dispatcher.add_handler(move_handler)




updater.start_polling()