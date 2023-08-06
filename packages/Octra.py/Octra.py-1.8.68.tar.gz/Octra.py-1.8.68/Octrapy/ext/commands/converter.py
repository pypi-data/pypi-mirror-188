"""
MIT License

Copyright (c) 2023 Akash

Octra ltd
"""

from .errors import BadArgument
from Octrapy.chat import Chat
from Octrapy.user import User
from Octrapy.errors import HTTPException

class Converter:
    """
    Base class for converters.
    """

    async def convert(self, ctx, arg):
        """
        Does the converting.
        """
        raise NotImplementedError

class UserConverter(Converter):
    """
    Converts an argument into a user.
    """

    async def convert(self, ctx, arg):
        try:
            arg = int(arg)
        except ValueError:
            raise BadArgument(arg, User, "Argument is not an ID")
        try:
            return await ctx.chat.get_member(arg)
        except HTTPException:
            raise BadArgument(arg, User, "Failed to fetch user")

class ChatConverter(Converter):
    """
    Converts an argument into a chat.
    """

    async def convert(self, ctx, arg):
        try:
            arg = int(arg)
        except ValueError:
            raise BadArgument(arg, Chat, "Argument is not an ID")
        try:
            return await ctx.bot.get_chat(arg)
        except HTTPException:
            raise BadArgument(arg, Chat, "Failed to fetch chat")
