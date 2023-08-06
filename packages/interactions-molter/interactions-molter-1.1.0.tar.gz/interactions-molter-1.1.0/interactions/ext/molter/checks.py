import typing

import interactions
from . import utils
from .command import MCT
from .command import MolterCommand
from .errors import CheckFailure

if typing.TYPE_CHECKING:
    from .context import MolterContext


__all__ = ("check", "has_permissions", "has_guild_permissions", "guild_only", "dm_only")


def check(
    check: typing.Callable[
        ["MolterContext"], typing.Coroutine[typing.Any, typing.Any, bool]
    ]
) -> typing.Callable[[MCT], MCT]:
    """
    Add a check to a command.

    Args:
        check (typing.Callable): A coroutine as a check for this command. It should take \
            a :class:`.MolterContext` and return a boolean.

    Returns:
        typing.Union[typing.Callable, MolterCommand]: The function or command decorated.
    """

    def wrapper(coro: MCT) -> MCT:
        if isinstance(coro, MolterCommand):
            coro.checks.append(check)
            return coro
        if not hasattr(coro, "checks"):
            coro.__checks__ = []  # type: ignore
        coro.__checks__.append(check)  # type: ignore
        return coro

    return wrapper


def has_permissions(
    *permissions: interactions.Permissions,
) -> typing.Callable[[MCT], MCT]:
    """
    A check to see if the author has permissions specified for the specific context.
    Considers guild ownership, roles, and channel overwrites.
    This does not take into account implicit permissions.
    Works for DMs.

    Args:
        permissions: A list of permissions to check.

    Returns:
        typing.Union[typing.Callable, MolterCommand]: The function or command decorated.
    """

    combined_permissions = interactions.Permissions(0)
    for perm in permissions:
        combined_permissions |= perm

    async def _permission_check(ctx: "MolterContext"):
        result = combined_permissions in ctx.author_permissions

        if not result:
            raise CheckFailure(
                ctx, "You do not have the proper permissions to use this command."
            )
        return result

    return check(_permission_check)


def has_guild_permissions(
    *permissions: interactions.Permissions,
) -> typing.Callable[[MCT], MCT]:
    """
    A check to see if the author has permissions specified for the guild.
    Considers guild ownership and roles.
    This does not take into account implicit permissions.
    Will fail in DMs.

    Args:
        permissions: A list of permissions to check.

    Returns:
        typing.Union[typing.Callable, MolterCommand]: The function or command decorated.
    """

    combined_permissions = interactions.Permissions(0)
    for perm in permissions:
        combined_permissions |= perm

    async def _permission_check(ctx: "MolterContext"):
        if not ctx.guild or isinstance(ctx.author, interactions.User):
            raise CheckFailure(ctx, "This command cannot be used in private messages.")

        result = combined_permissions in utils.guild_permissions(ctx.author, ctx.guild)

        if not result:
            raise CheckFailure(
                ctx, "You do not have the proper permissions to use this command."
            )
        return result

    return check(_permission_check)


def guild_only() -> typing.Callable[[MCT], MCT]:
    """
    A check to make the command only run in guilds.

    Returns:
        typing.Union[typing.Callable, MolterCommand]: The function or command decorated.
    """

    async def _guild_check(ctx: "MolterContext"):
        if not ctx.guild_id:
            raise CheckFailure(ctx, "This command cannot be used in private messages.")
        return True

    return check(_guild_check)


def dm_only() -> typing.Callable[[MCT], MCT]:
    """
    A check to make the command only run in DMs.

    Returns:
        typing.Union[typing.Callable, MolterCommand]: The function or command decorated.
    """

    async def _guild_check(ctx: "MolterContext"):
        if ctx.guild_id:
            raise CheckFailure(
                ctx, "This command can only be used in private messages."
            )
        return True

    return check(_guild_check)
