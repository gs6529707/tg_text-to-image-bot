import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TELEGRAM_BOT_TOKEN = os.getenv("token") 
CLIPDROP_API_KEY = os.getenv("api")  
CLIPDROP_API_URL = "https://clipdrop-api.co/text-to-image/v1"  

async def generate_image(prompt: str) -> str:
    try:
        headers = {
            "x-api-key": CLIPDROP_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {"prompt": prompt}
        response = requests.post(CLIPDROP_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            image_path = "generated_image.png"
            with open(image_path, "wb") as file:
                file.write(response.content)
            return image_path
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the Gaurav's Image Generator Bot! Send me a prompt, and I'll create an image for you.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text
    await update.message.reply_text("Generating your image... Please wait.")
    image_path = await generate_image(prompt)
    if image_path.startswith("Error"):
        await update.message.reply_text(image_path)
    else:
        with open(image_path, "rb") as file:
            await update.message.reply_photo(photo=file, caption="Here is your image!")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
