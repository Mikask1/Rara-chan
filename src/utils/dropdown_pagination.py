import discord
from discord.commands.commands import option
from discord.ext.pages import Paginator

class _Dropdown(discord.ui.Select):
    def __init__(self, placeholder: str, options: list, paginator: Paginator):   
        self.paginator = paginator
        
        self.label_index = {}
        for n, option in enumerate(options):
            self.label_index[option.label] = n

        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        page_number = self.label_index[self.values[0]]
        self.paginator.current_page = page_number
        await self.paginator.goto_page(interaction, page_number=page_number)

class _DropdownView(discord.ui.View):
    def __init__(self, placeholder: str, options: list, paginator: Paginator):
        super().__init__()

        dropdown = _Dropdown(placeholder=placeholder, paginator=paginator, options=options)

        super().add_item(dropdown)

class DropdownPaginator(Paginator):
    def __init__(
                self: Paginator, 
                page_list: list, 
                dropdown_placeholder: str, 
                options: list, 
                show_indicator= True, 
                show_disabled= True,
                ):

        self.pages = page_list
        
        view = _DropdownView(paginator=self, placeholder=dropdown_placeholder, options=options)

        super().__init__(pages=self.pages, custom_view=view, show_indicator=show_indicator, show_disabled=show_disabled)
