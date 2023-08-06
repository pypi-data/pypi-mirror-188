"""
MIT License

Copyright (c) 2023 Akash

Octra ltd
"""

import datetime

from .chat import Chat
from .user import User
from .abc import OctraObject


class Message(OctraObject):
    """
    Represents a message in Octra.

    .. container:: operations

        .. describe:: x == y

            Checks if two messages are equal.

        .. describe:: x != y

            Checks if two messages are not equal.

    Attributes
    ----------
    id: :class:`int`
        The ID of the message.
    created_at: :class:`datetime.datetime`
        The time the message was created.
    edited_at: Optional[:class:`datetime.datetime`]
        The time the message was edited.
    content: :class:`str`
        The content of the message.
    chat: :class:`Octrapy.Chat`
        The chat the message is in.
    author: :class:`Octrapy.User`
        The author of the message.
    """

    def __init__(self, http, data: dict):
        super().__init__(http, data)
        self.id = data.get("message_id")

        self.created_at = data.get("date")
        if self.created_at:
            datetime.datetime.fromtimestamp(self.created_at)

        self.edited_at = data.get("edit_date")
        if self.edited_at:
            datetime.datetime.fromtimestamp(self.edited_at)

        self.content = data.get("text")

        if "chat" in data:
            self.chat = Chat(http, data.get("chat"))
        else:
            self.chat = None

        if "from" in data:
            self.author = User(http, data.get("from"))
        else:
            self.author = None

    async def reply(self, content: str, parse_mode: str = None):
        """|coro|
        
        Replys to the message.

        Parameters
        ----------
        content: :class:`str`
            The content of the message to send.
        parse_mode: :class:`str`
            The parse mode of the message to send.

        Returns
        -------
        :class:`Octrapy.Message`
            The message sent.

        Raises
        ------
        :exc:`Octrapy.HTTPException`
            Sending the message failed.
        """

        return await self._http.send_message(chat_id=self.chat.id, content=content, parse_mode=parse_mode, reply_message_id=self.id)

    async def forward(self, destination):
        """|coro|
        
        Forwards the message to a destination.

        Parameters
        ----------
        destination: :class:Octrapy.Chat`
            The chat forward the message to.
        
        Returns
        -------
        :class:`Octrapy.Message`
            The message sent.
        
        Raises
        ------
        :exc:`Octrapy.HTTPException`
            Forwarding the message failed.
        """

        return await self._http.forward_message(chat_id=destination.id, from_chat_id=self.chat.id, message_id=self.id)

    async def edit(self, content: str, parse_mode: str = None):
        """|coro|

        Edits the message.

        Parameters
        ----------
        content: :class:`str`
            The content of the new message.
        parse_mode: :class:`str`
            The parse mode of the new message.

        Raises
        ------
        :exc:`Octrapy.HTTException`
            Editing the message failed.
        """

        await self._http.edit_message_content(chat_id=self.chat.id, message_id=self.id, content=content, parse_mode=parse_mode)

    async def delete(self):
        """|coro|

        Deletes the message.

        Raises
        ------
        :exc:`Octrapy.HTTPException`
            Deleting the message failed.
        """

        return await self._http.delete_message(chat_id=self.chat.id, message_id=self.id)
