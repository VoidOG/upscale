import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = "7382235042:AAFv5nrAHJEnq3cuJUOTCGLKYdVDeIaYZnE"
PICSART_UPSCALE_API_TOKEN = "eyJraWQiOiI5NzIxYmUzNi1iMjcwLTQ5ZDUtOTc1Ni05ZDU5N2M4NmIwNTEiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhdXRoLXNlcnZpY2UtMmQyNjhkYjItZjI4NC00NWZmLWJmZWItNjE3ZTRkZjFhZGFiIiwiYXVkIjoiMzg4ODQ3MTMxMDIzMTAxIiwibmJmIjoxNzI5MTk5NzYxLCJzY29wZSI6WyJiMmItYXBpLmdlbl9haSIsImIyYi1hcGkuaW1hZ2VfYXBpIl0sImlzcyI6Imh0dHBzOi8vYXBpLnBpY3NhcnQuY29tL3Rva2VuLXNlcnZpY2UiLCJvd25lcklkIjoiMzg4ODQ3MTMxMDIzMTAxIiwiaWF0IjoxNzI5MTk5NzYxLCJqdGkiOiI2MTFkN2EyNS01Zjk3LTRkYTktYjczZC02MmRmZGM4MTUxMGMifQ.Se0Jb6kDbE0-c49r33uIYOhx7Aj7Nj0qatUMHQ8KfI3MPUSbyG89hluKPuzwkZX8y0165IIUr8wHQGKlscVbuYOAOa8MsEVS0Za6eJRsnYZyl5iPvz50vDBdFTZJhhBhjfbvU5wUPtQ1UsLwLAOMxuQCbkVHyRG8IEXcdrnwzjJCoI2aTNiewBm2nG_oL0dM8wdL9hfyqisZwC3qB1bURHnscxKLKxK2yPtdaQDSN8Rg_fEPh1i3J_fJjlXvrq0QvjuPAyiWPVVDZ90K6AALwB34LPp2kME-xU5aAbn2rmchk-IN-zu8PbjVTtAjCHrisRRV_v6-bMgd8bOq_2Kacw"

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! Send me an image to upscale using Picsart.')

def handle_image(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]  # Get the best resolution
    file = photo.get_file()
    file_path = file.download()

    with open(file_path, 'rb') as image_file:
        headers = {
            'Authorization': f'Bearer {PICSART_UPSCALE_API_TOKEN}',
            'Content-Type': 'multipart/form-data'
        }
        files = {'file': image_file}
        response = requests.post(
            'https://api.picsart.com/upscale',
            headers=headers,
            files=files
        )

    if response.status_code == 200:
        upscaled_image_url = response.json().get('url')  
        update.message.reply_photo(photo=upscaled_image_url)
    else:
        update.message.reply_text('Failed to upscale the image. Please try again later.')
def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
