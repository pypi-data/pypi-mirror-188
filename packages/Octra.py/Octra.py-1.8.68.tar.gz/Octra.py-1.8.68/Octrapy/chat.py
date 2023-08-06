"""
MIT License

Copyright (c) 2023 Akash

Octra ltd
"""

from .errors import *
from .file import *
from .abc import OctraObject


class Chat(OctraObject):
    """
    Represents a chat in Octra.

    .. container:: operations

        .. describe:: x == y

            Checks if two chats are equal.

        .. describe:: x != y

            Checks if two chats are not equal.

        .. describe:: str(x)

            Returns the chat's title.


    Attributes
    ----------
    id: :class:`int`
        The ID of the chat.
    title: :class:`str`
        The title of the chat.
    description: Optional[:class:`str`]
        The description of the chat.
    type: :class:`str`
        The type of the chat.
    """

    def __init__(self, http, data: dict):
        super().__init__(http, data)
        self.title = data.get("title")
        self.username = data.get("username")
        self.description = data.get("description")
        self.type = data.get("type")

    def __str__(self):
        return self.title

    async def send(self, content: str = None, file: File = None, parse_mode: str = None):
        """|coro|

        Sends a message to the chat.

        Parameters
        ----------
        content: :class:`str`
            The content of the message to send.
        file: :class:`Octrapy.File`
            The file to send.
        parse_mode: :class:`str`
            The parse mode of the message to send.

        Returns
        -------
        :class:`Octrapy.Message`
            The message sent.

        Raises
        ------
        :exc:`errors.HTTPException`
            Sending the message failed.
        """

        if not file:
            return await self._http.send_message(chat_id=self.id, content=content, parse_mode=parse_mode)
        else:
            if isinstance(file, Document):
                return await self._http.send_document(chat_id=self.id, document=file.file, filename=file.filename)

            elif isinstance(file, Photo):
                return await self._http.send_photo(chat_id=self.id, photo=file.file, filename=file.filename, caption=file.caption)

    async def send_poll(self, question: str, options: list):
        """|coro|

        Sends a poll to the chat.

        Parameters
        ----------
        question: :class:`str`
            The question of the poll.
        options: :class:`list`
            The options in the poll.

        Returns
        -------
        :class:`Octrapy.Poll`
            The poll sent.

        Raises
        ------
        :exc:`Octrapy.HTTPException`
            Sending the poll failed.
        """

        return await self._http.send_poll(chat_id=self.id, question=question, options=options)

    async def send_action(self, action: str):
        """|coro|

        Sends an action to the chat.

        Parameters
        ----------
        action: :class:`str`
            The action to send.

        Raises
        ------
        :exc:`Octrapy.HTTPException`
            Sending the action failed.
        """

        await self._http.send_chat_action(chat_id=self.id, action=action)

    async def get_member(self, user_id: int):
        """|coro|

        Fetches a member in the chat.

        Parameters
        ----------
        user_id: :class:`int`
            The user ID of the member.

        Returns
        -------
        :class:`Octrapy.User`
            The member fetched.

        Raises
        ------
        :exc:`Octrapy.HTTPException`
            Fetching the member failed.
        """

        return await self._http.get_chat_member(chat_id=self.id, user_id=user_id)

    @property
    def history(self):
        """
        :class:`list`:
            The cached messages in the chat.
        """

        return [x for x in self._http.messages if x.chat.id == self.id]

    def fetch_message(self, message_id: int):
        """
        Fetches a message from the cache.

        Parameters
        ----------
        message_id: :class:`int`
            The ID of the message to fetch.

        Returns
        -------
        :class:`chat.Message`
            The message fetched.
        """

        for x in self.history:
            if x.id == message_id:
                return x
