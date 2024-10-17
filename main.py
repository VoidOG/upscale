import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# PicsArt.io API token
PICSART_API_TOKEN = "eyJraWQiOiI5NzIxYmUzNi1iMjcwLTQ5ZDUtOTc1Ni05ZDU5N2M4NmIwNTEiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhdXRoLXNlcnZpY2UtZDA1ODg0OTItN2E2MS00Y2RmLTkyZDMtNGUyODFhNTM4MjIyIiwiYXVkIjoiMzg4ODQ3MTMxMDIzMTAxIiwibmJmIjoxNzI5MjAwNzg3LCJzY29wZSI6WyJiMmItYXBpLmdlbl9haSIsImIyYi1hcGkuaW1hZ2VfYXBpIl0sImlzcyI6Imh0dHBzOi8vYXBpLnBpY3NhcnQuY29tL3Rva2VuLXNlcnZpY2UiLCJvd25lcklkIjoiMzg4ODQ3MTMxMDIzMTAxIiwiaWF0IjoxNzI5MjAwNzg3LCJqdGkiOiIzZDViMDM0YS04M2YyLTQ5NTMtYmYzMy1iMDE3MGI0N2EyY2EifQ.I-z_LbPpQ7EWZyENtX_MLBNM5ntAYgC4tLC-68d2rGWS0Q99plpZEnjx4ylRIvwfpT2WWmtMANEiagNj-2t8kq6BILmC3lSe-ib1MccwGqvAZTARrc218ue88ePyX_TScpf--mgNgNrYcscxv6anbeZrFeQoGg1LwQViHBmv41yU39WPaDbTcIC2wyK-62SU4xSqqb9hd-vBskRByHaMLeYvV4f7X6d5cQ2CNQ_cQtQhDUmO3-Sjz1mtSg982_C8QLyUfrVY7fcXBWHM2n97KzVpC-78TSFwNm5JtINQU9y2-KJf0hs0DqWOMXtthSTWihT9pJiWD5K0gRZrg04fzQ"

# PicsArt.io upscale API URL
PICSART_API_URL = "https://api.picsart.io/tools/upscale"

# Command to start the bot
def start(update: Update, context):
    update.message.reply_text("Send me an image, and I'll upscale it using PicsArt.io!")

# Function to upscale the image using PicsArt.io API
def upscale_image(image_path):
    headers = {
        'Authorization': f'Bearer {PICSART_API_TOKEN}',
        'Content-Type': 'multipart/form-data'
    }
    
    files = {
        'image': open(image_path, 'rb')
    }
    
    # Send the request to the PicsArt.io upscale API
    response = requests.post(PICSART_API_URL, headers=headers, files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()['data']['output_url']  # Assuming the API returns this
    else:
        return None

# Function to handle image uploads
def handle_image(update: Update, context):
    # Get the image file sent by the user
    image_file = update.message.photo[-1].get_file()  # Get the highest resolution photo
    
    # Download the image locally
    image_path = "user_image.jpg"
    image_file.download(image_path)
    
    # Call the PicsArt.io API to upscale the image
    upscaled_image_url = upscale_image(image_path)
    
    if upscaled_image_url:
        # Send the upscaled image back to the user
        update.message.reply_text(f"Here is your upscaled image: {upscaled_image_url}")
    else:
        update.message.reply_text("Failed to upscale the image. Please try again.")

# Main function to set up the bot
def main():
    # Your Telegram bot token
    TELEGRAM_BOT_TOKEN = "7382235042:AAFv5nrAHJEnq3cuJUOTCGLKYdVDeIaYZnE"

    # Set up the updater and dispatcher
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handler to start the bot
    dispatcher.add_handler(CommandHandler("start", start))

    # Handler for images
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
