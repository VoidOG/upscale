import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Bot token from BotFather
BOT_TOKEN = '7382235042:AAFv5nrAHJEnq3cuJUOTCGLKYdVDeIaYZnE'
PICSART_UPSCALE_API_TOKEN = 'eyJraWQiOiI5NzIxYmUzNi1iMjcwLTQ5ZDUtOTc1Ni05ZDU5N2M4NmIwNTEiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhdXRoLXNlcnZpY2UtZDA1ODg0OTItN2E2MS00Y2RmLTkyZDMtNGUyODFhNTM4MjIyIiwiYXVkIjoiMzg4ODQ3MTMxMDIzMTAxIiwibmJmIjoxNzI5MjAwNzg3LCJzY29wZSI6WyJiMmItYXBpLmdlbl9haSIsImIyYi1hcGkuaW1hZ2VfYXBpIl0sImlzcyI6Imh0dHBzOi8vYXBpLnBpY3NhcnQuY29tL3Rva2VuLXNlcnZpY2UiLCJvd25lcklkIjoiMzg4ODQ3MTMxMDIzMTAxIiwiaWF0IjoxNzI5MjAwNzg3LCJqdGkiOiIzZDViMDM0YS04M2YyLTQ5NTMtYmYzMy1iMDE3MGI0N2EyY2EifQ.I-z_LbPpQ7EWZyENtX_MLBNM5ntAYgC4tLC-68d2rGWS0Q99plpZEnjx4ylRIvwfpT2WWmtMANEiagNj-2t8kq6BILmC3lSe-ib1MccwGqvAZTARrc218ue88ePyX_TScpf--mgNgNrYcscxv6anbeZrFeQoGg1LwQViHBmv41yU39WPaDbTcIC2wyK-62SU4xSqqb9hd-vBskRByHaMLeYvV4f7X6d5cQ2CNQ_cQtQhDUmO3-Sjz1mtSg982_C8QLyUfrVY7fcXBWHM2n97KzVpC-78TSFwNm5JtINQU9y2-KJf0hs0DqWOMXtthSTWihT9pJiWD5K0gRZrg04fzQ'

# Function to handle the start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! Send me an image to upscale using Picsart.')

# Function to handle image uploads
def handle_image(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]  # Get the best resolution
    file = photo.get_file()
    file_path = file.download()

    # Send the image to Picsart Upscale API
    with open(file_path, 'rb') as image_file:
        headers = {
            'Authorization': f'Bearer {PICSART_UPSCALE_API_TOKEN}',
            'Content-Type': 'multipart/form-data'
        }
        files = {'file': image_file}
        try:
            response = requests.post(
                'https://api.picsart.com/upscale',  # Replace with correct endpoint
                headers=headers,
                files=files
            )
            print(response.text)  # For debugging
        except Exception as e:
            update.message.reply_text(f"Error: {e}")
            return

    # Handle response
    if response.status_code == 200:
        upscaled_image_url = response.json().get('url')  # Example response format
        update.message.reply_photo(photo=upscaled_image_url)
    else:
        error_message = response.json().get('error', 'Unknown error occurred')
        update.message.reply_text(f"Failed to upscale the image: {error_message}")

# Function to handle errors
def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

def main():
    # Initialize the bot
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Handlers for start command and image messages
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

    # Log errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
