from typing import Optional, Union

import disnake
import disnake.ext.commands


DELETE_ID_V2 = "message_delete_button_v2:"


class DeleteButton(disnake.ui.Button):
    """A button that when pressed, has a listener that will delete the message."""

    def __init__(
        self,
        user: Union[int, disnake.User, disnake.Member],
        *,
        allow_manage_messages: bool = True,
        initial_message: Optional[Union[int, disnake.Message]] = None,
        style: Optional[disnake.ButtonStyle] = None,
        emoji: Optional[Union[disnake.Emoji, disnake.PartialEmoji, str]] = None,
    ):
        if isinstance(user, (disnake.User, disnake.Member)):
            user_id = user.id
        else:
            user_id = user

        super().__init__()
        self.custom_id = DELETE_ID_V2
        permissions = disnake.Permissions()
        if allow_manage_messages:
            permissions.manage_messages = True
        self.custom_id += str(permissions.value) + ":"
        self.custom_id += str(user_id)

        self.custom_id += ":"
        if initial_message:
            if isinstance(initial_message, disnake.Message):
                initial_message = initial_message.id
            self.custom_id += str(initial_message)

        # set style based on if the message was provided
        if style is None:
            if initial_message:
                self.style = disnake.ButtonStyle.danger
            else:
                self.style = disnake.ButtonStyle.secondary
        else:
            self.style = style

        # set emoji based on the style
        if emoji is None:

            self.emoji = ":trashcan_on_red:976669056587415592"
        else:
            self.emoji = emoji
