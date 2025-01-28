import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# API keys and endpoints
TELEGRAM_BOT_TOKEN = os.getenv("token")"  # Replace with your Telegram bot token
CLIPDROP_API_KEY = os.getenv("api")  # Replace with your ClipDrop API key
CLIPDROP_API_URL = "https://clipdrop-api.co/text-to-image/v1"  # ClipDrop API endpoint

# Function to generate image using ClipDrop API
async def generate_image(prompt: str) -> str:
    try:
        headers = {
            "x-api-key": CLIPDROP_API_KEY,
            "Content-Type": "application/json",
        }

        # Payload with the text prompt
        payload = {"prompt": prompt}

        # Send POST request to ClipDrop API
        response = requests.post(CLIPDROP_API_URL, json=payload, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            # Save the image to a file
            image_path = "generated_image.png"
            with open(image_path, "wb") as file:
                file.write(response.content)
            return image_path
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

# Command handler to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Gaurav's Image Generator Bot! Send me a prompt, and I'll create an image for you."
    )

# Message handler to process user prompts and generate images
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text
    await update.message.reply_text("Generating your image... Please wait.")
    
    # Generate the image using ClipDrop API
    image_path = await generate_image(prompt)
    
    # Check if an error occurred
    if image_path.startswith("Error"):
        await update.message.reply_text(image_path)
    else:
        # Send the generated image back to the user
        with open(image_path, "rb") as file:
            await update.message.reply_photo(photo=file, caption="Here is your image!")

# Main function to set up the bot and run it
def main():
    # Create the bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling for updates
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
