from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
import os
from helper.database import db

@Client.on_message(filters.channel & filters.media & ~filters.photo)
async def channel_media_handler(bot: Client, message: Message):
    try:
        # Get custom caption and thumbnail from database
        custom_caption = await db.get_caption(message.from_user.id)
        custom_thumb = await db.get_thumbnail(message.from_user.id)
        
        # Download the media
        media = await message.download()
        
        # Prepare caption
        if custom_caption:
            caption = custom_caption
        else:
            caption = message.caption if message.caption else ""
        
        # Send the media with custom caption and thumbnail
        if message.video:
            await message.edit_media(
                media=media,
                caption=caption,
                thumb=custom_thumb if custom_thumb else None
            )
        elif message.document:
            await message.edit_media(
                media=media,
                caption=caption,
                thumb=custom_thumb if custom_thumb else None
            )
        elif message.audio:
            await message.edit_media(
                media=media,
                caption=caption,
                thumb=custom_thumb if custom_thumb else None
            )
        
        # Clean up downloaded media
        if os.path.exists(media):
            os.remove(media)
            
    except Exception as e:
        print(f"Error in channel media handler: {e}")
        return 
