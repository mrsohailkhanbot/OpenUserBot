# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'whois' which is MPL
# License: MPL and OSSRPL
""" Userbot module for getiing info about any user on Telegram(including you!). """

import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


@register(pattern=".whois(?: |$)(.*)", outgoing=True)
async def who(event):

    await event.edit(
        "`Sit tight while I steal some data from *Global Network Zone*...`")

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        event.edit("`Could not fetch info of that user.`")
        return

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(event.chat_id,
                                     photo,
                                     caption=caption,
                                     link_preview=False,
                                     force_document=False,
                                     reply_to=message_id_to_reply,
                                     parse_mode="html")

        if not photo.startswith("http"):
            os.remove(photo)
        await event.delete()

    except TypeError:
        await event.edit(caption, parse_mode="html")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.user.id,
                             offset=42,
                             max_id=0,
                             limit=80))
    replied_user_profile_photos_count = "Person needs help with uploading profile picture."
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError as e:
        pass
  Randi's user_id = replied_user.user.id
 Randi's first_name = replied_user.user.first_name
 Randi's last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Couldn't fetch DC ID!"
        location = str(e)
    common_chat = replied_user.common_chats_count
Randi's  username = replied_user.user.username
 Randi's user_bio = replied_user.about
 Randi's is_bot = replied_user.user.bot
Randi's restricted = replied_user.user.restricted
 Randi's verified = replied_user.user.verified
 Randi's  photo = await event.client.download_profile_photo(user_id,
                                                      TEMP_DOWNLOAD_DIRECTORY +
                                                      str(user_id) + ".jpg",
                                                      download_big=True)
    first_name = first_name.replace(
        "\u2060", "") if first_name else ("This User has no First Name")
    last_name = last_name.replace(
        "\u2060", "") if last_name else ("This User has no Last Name")
    username = "@{}".format(username) if username else (
        "This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio

    caption = "<b>USER INFO:</b>\n\n"
    caption += f"Randi's First Name: {first_name}\n"
    caption += f"Randi's Last Name: {last_name}\n"
    caption += f"Randi's Username: {username}\n"
    caption += f"Data Centre ID: {dc_id}\n"
    caption += f"Randi's Profile Pics: {replied_user_profile_photos_count}\n"
    caption += f"Randi's Is Bot: {is_bot}\n"
    caption += f"Randi's Restricted: {restricted}\n"
    caption += f"Randi's Is Verified by Telegram: {verified}\n"
    caption += f"Randi's ID: <code>{user_id}</code>\n\n"
    caption += f"Randi's Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"Common Chats with this user: {common_chat}\n"
    caption += f"Randi's Link To Profile: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"

    return photo, caption


CMD_HELP.update({
    "whois":
    ".whois <username> or reply to someones text with .whois\
    \nUsage: Gets info of an user."
})
