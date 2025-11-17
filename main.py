import os
import chess
import chess.engine
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# .env faylidan tokenni o‘qish
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Stockfish yo‘li (Railway’ga moslashtirish mumkin)
STOCKFISH_PATH = "/usr/games/stockfish"  # keyin Railway’da aniqlash kerak

# /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "♟ Chess Helper Bot!\nFEN yoki move yuboring.\n/help yozing."
    )

# /help buyrug‘i
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Move misol: e2e4\nFEN misol: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )

# Move yoki FENni qabul qilish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    board = chess.Board()
    try:
        if " " in user_text and "/" in user_text:
            board.set_fen(user_text)
        else:
            board.push_uci(user_text)
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")
        return

    try:
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            best_move = result.move
            await update.message.reply_text(f"Eng yaxshi yurish: {best_move}")
    except Exception as e:
        await update.message.reply_text(f"Stockfish bilan xato: {e}")

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
