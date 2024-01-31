import os
import random
import string
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram.error import BadRequest

bot_token = os.environ.get("BOT_TOKEN")
# EMAIL, PASSWORD, TOKEN, MEGA_EMAIL, MEGA_PASSWORD, KOOFR_EMAIL, KOOFR_PASSWORD = range(7)
services = ["PIKPAK_EMAIL", "PIKPAK_PASSWORD", "TELEBOX_TOKEN", "MEGA_EMAIL", "MEGA_PASSWORD", "KOOFR_EMAIL", "KOOFR_PASSWORD", "PROTON_EMAIL", "PROTON_PASSWORD", "JOTTA_TOKEN"]
credentials = range(len(services))

for service, credential in zip(services, credentials):
    globals()[service] = credential


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        '<b>⚙️ Welcome to Canon Rclone Bot 🧰 </b>\n\n'
        '🤔 What does this bot do?\n'
        '- This bot is to easily generate Rclone config for PikPak, Telebox, Mega, and Koofr (for now).\n'
        '🤷‍♂️ Does it support Google Drive, Dropbox, and other cloud storages?\n'
        '- It depends. If the config generation doesn\'t need web auth, then it can be added. Sadly, Google Drive and Dropbox uses web auth so those services can\'t be generated with this bot.\n'
        '🔐 Will my token, email, and password be logged?\n'
        '- This bot doesn\'t log your credentials to generate the config (the log only saves successful or error messages) and it will delete any files related to your account after the config is being sent to you. If you don\'t trust this bot, you can use a dummy account or you may simply not use this bot.\n'
        '❌ How to cancel current operations?\n'
        '- For now, simply leave it that way or enter random inputs until it gives you a config or an error. You can also trigger another command instead if you choose the wrong command. This is a bug in my code and I haven\'t found the solution yet, sorry for the inconvenience.\n\n'
        '<b>How to use this bot?</b>\n'
        '/telebox: Generate Telebox Rclone config\n'
        '/pikpak: Generate PikPak Rclone config\n'
        '/mega: Generate Mega Rclone config\n'
        '/koofr: Generate Koofr Rclone config\n'
        '/proton: Generate Proton Drive Rclone config\n'
        '/jotta: Generate Jottacloud Rclone config\n'
        '/help: Show this message\n\n'
        '👩🏻 Author: @katarina_ox (<a href="https://github.com/devolart/rclone-generator-bot" rel="noopener noreferrer" target="_blank">source code</a>)',
        parse_mode='HTML',
        disable_web_page_preview=True
    )

def koofr(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your Koofr email:')
    return KOOFR_EMAIL

def koofr_email(update: Update, context: CallbackContext) -> int:
    context.user_data['koofr_email'] = update.message.text
    update.message.reply_text('Please enter your Koofr app password: (visit https://app.koofr.net/app/admin/preferences/password and generate an app password)')
    return KOOFR_PASSWORD

def koofr_password(update: Update, context: CallbackContext) -> int:
    context.user_data['koofr_password'] = update.message.text
    generate_config(update, context, 'koofr', 'koofr', 'user', context.user_data['koofr_email'], 'password', context.user_data['koofr_password'])
    return ConversationHandler.END

def proton(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your Proton email:')
    return PROTON_EMAIL

def proton_email(update: Update, context: CallbackContext) -> int:
    context.user_data['proton_email'] = update.message.text
    update.message.reply_text('Please enter your Proton password:')
    return PROTON_PASSWORD

def proton_password(update: Update, context: CallbackContext) -> int:
    context.user_data['proton_password'] = update.message.text
    generate_config(update, context, 'protondrive', 'protondrive', 'username', context.user_data['proton_email'], 'password', context.user_data['proton_password'])
    return ConversationHandler.END

def jotta(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your token: (visit https://www.jottacloud.com/web/secure and generate a personal login token. Note: you only have access to archive section)')
    return JOTTA_TOKEN

def jotta_token(update: Update, context: CallbackContext) -> int:
    context.user_data['jotta_token'] = update.message.text
    generate_config(update, context, 'jottacloud', 'jottacloud', 'config_login_token', context.user_data['jotta_token'])
    return ConversationHandler.END

def mega(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your Mega email:')
    return MEGA_EMAIL

def mega_email(update: Update, context: CallbackContext) -> int:
    context.user_data['mega_email'] = update.message.text
    update.message.reply_text('Please enter your Mega password:')
    return MEGA_PASSWORD

def mega_password(update: Update, context: CallbackContext) -> int:
    context.user_data['mega_password'] = update.message.text
    generate_config(update, context, 'mega', 'mega', 'user', context.user_data['mega_email'], 'pass', context.user_data['mega_password'])
    return ConversationHandler.END

def pikpak(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your email:')
    return PIKPAK_EMAIL

def pikpak_email(update: Update, context: CallbackContext) -> int:
    context.user_data['pikpak_email'] = update.message.text
    update.message.reply_text('Please enter your password:')
    return PIKPAK_PASSWORD

def pikpak_password(update: Update, context: CallbackContext) -> int:
    context.user_data['pikpak_password'] = update.message.text
    generate_config(update, context, 'pikpak', 'pikpak', 'user', context.user_data['pikpak_email'], 'pass', context.user_data['pikpak_password'])
    return ConversationHandler.END

def telebox(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your token: (visit https://www.telebox.online/admin/account)')
    return TELEBOX_TOKEN

def telebox_token(update: Update, context: CallbackContext) -> int:
    context.user_data['telebox_token'] = update.message.text
    generate_config(update, context, 'telebox', 'linkbox', 'token', context.user_data['telebox_token'])
    return ConversationHandler.END

def generate_config(update: Update, context: CallbackContext, name: str, type: str, param1: str, value1: str, param2: str = None, value2: str = None) -> None:
    loading_message = update.message.reply_text('Loading...')
    folder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    os.makedirs(folder_name, exist_ok=True)
    try:
        command = f'./rclone config create {name} {type} {param1} "{value1}"'
        if param2 and value2:
            command += f' {param2} "{value2}"'
        command += f' --config {folder_name}/rclone.conf'
        subprocess.check_output(command, shell=True)
        with open(f'{folder_name}/rclone.conf', 'r') as f:
            config_content = f.read()
        try:
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(f'{folder_name}/rclone.conf', 'rb'), caption=f'```\n{config_content}\n```', parse_mode='MarkdownV2')
        except:
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(f'{folder_name}/rclone.conf', 'rb'), caption=f'```\nConfig is too long, no captions for this config\n```', parse_mode='MarkdownV2')
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f'Error: {str(e)}')
    finally:
        os.remove(f'{folder_name}/rclone.conf')
        os.rmdir(folder_name)
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loading_message.message_id)

def main() -> None:
    updater = Updater(bot_token)

    pikpak_handler = ConversationHandler(
        entry_points=[CommandHandler('pikpak', pikpak)],
        states={
            PIKPAK_EMAIL: [MessageHandler(Filters.text & ~Filters.command, pikpak_email)],
            PIKPAK_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, pikpak_password)],
        },
        fallbacks=[],
    )

    telebox_handler = ConversationHandler(
        entry_points=[CommandHandler('telebox', telebox)],
        states={
            TELEBOX_TOKEN: [MessageHandler(Filters.text & ~Filters.command, telebox_token)],
        },
        fallbacks=[],
    )

    mega_handler = ConversationHandler(
        entry_points=[CommandHandler('mega', mega)],
        states={
            MEGA_EMAIL: [MessageHandler(Filters.text & ~Filters.command, mega_email)],
            MEGA_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, mega_password)],
        },
        fallbacks=[],
    )

    koofr_handler = ConversationHandler(
        entry_points=[CommandHandler('koofr', koofr)],
        states={
            KOOFR_EMAIL: [MessageHandler(Filters.text & ~Filters.command, koofr_email)],
            KOOFR_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, koofr_password)],
        },
        fallbacks=[],
    )

    proton_handler = ConversationHandler(
        entry_points=[CommandHandler('proton', proton)],
        states={
            PROTON_EMAIL: [MessageHandler(Filters.text & ~Filters.command, proton_email)],
            PROTON_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, proton_password)],
        },
        fallbacks=[],
    )

    jotta_handler = ConversationHandler(
        entry_points=[CommandHandler('jotta', jotta)],
        states={
            JOTTA_TOKEN: [MessageHandler(Filters.text & ~Filters.command, jotta_token)],
        },
        fallbacks=[],
    )

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', start))
    updater.dispatcher.add_handler(pikpak_handler)
    updater.dispatcher.add_handler(telebox_handler)
    updater.dispatcher.add_handler(mega_handler)
    updater.dispatcher.add_handler(koofr_handler)
    updater.dispatcher.add_handler(proton_handler)
    updater.dispatcher.add_handler(jotta_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
