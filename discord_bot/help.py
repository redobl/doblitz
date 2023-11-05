from discord.ext import commands


def usage_str(ctx):
    command = ctx.command
    if len(command.aliases) > 0:
        aliases = "|".join(command.aliases)
        return (
            f"Использование: `{ctx.prefix}[{command.name}|{aliases}] {command.usage}`"
        )
    else:
        return f"Использование: `{ctx.prefix}{command.name} {command.usage}`"


class HelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self) -> str:
        return (
            "Для получения информации о команде используй .помоги <команда>\n"
            "Для получения информации о категории используй .помоги <категория>"
        )

    def command_not_found(self, string: str) -> str:
        return f"Команда или категория {string} не найдена."

    def subcommand_not_found(self, command: commands.Command, string: str) -> str:
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"Команда {command.qualified_name} не имеет подкоманды с названием {string}."
        return f"Команда {command.qualified_name} не имеет подкоманд."

    def __init__(self):
        super().__init__(
            arguments_heading="Аргументы:",
            commands_heading="Команды:",
            default_argument_description="Нет описания.",
            no_category="Без категории",
            show_parameter_descriptions=False,
            command_attrs={
                "name": "помоги",
                "aliases": ["помощь", "хелп", "help"],
                "help": "Показывает это сообщение.",
                "brief": "Показывает это сообщение.",
                "usage": "[команда]",
            },
        )
