import subprocess

from telegram import Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import ContextTypes

async def get_version_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    short_id = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"]
    ).decode().strip()
    commit_date = subprocess.check_output(
        ["git", "show", "-s", "--format=%cd", "--date=format:%Y/%m/%d %H:%M", "HEAD"]
    ).decode().strip()
    await update.message.reply_text("每日沙雕墙 投稿机器人 V2\n\n使用 \\/help 获取帮助。\n\n版本：`"+short_id+"`\n日期："+escape_markdown(commit_date)+"\nGitHub：[仓库地址](https://github.com/moehanabi/tg-reviewer-bot)", parse_mode=ParseMode.MARKDOWN_V2)

async def get_help_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用投稿机器人。\n\n需要投稿的话，直接发送给我就行，我会把消息发送给审核。")