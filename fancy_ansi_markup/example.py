import ansimarkup

from fancy_ansi_markup.src.fancy_ansi_markup import FancyAnsiMarkup

our_tags = {
    "important": ansimarkup.parse("<red><b>"),
    "warning": ansimarkup.parse("<yellow><b>")
}

fam: FancyAnsiMarkup = FancyAnsiMarkup(
    tags=our_tags,
    always_reset=True,
    strict=True
)

fam.print_with_bg_color(text="Hello", bg_color="#DDDDDD")
fam.print_with_bg_color(text="World", bg_color="#DDDDDD")

fam.print_with_bg_color(text="Hello", bg_color="green")
fam.print_with_bg_color(text="World", bg_color="green")

fam.print_with_bg_color(text="Hello", bg_color="yellow", line_length=60)
fam.print_with_bg_color(text="World", bg_color="yellow", line_length=60)

fam.print_newlines(n=2)

for i in range(1,10):
    fam.print_for_row(text="<important>TEXT 1</important>", row=i)
    fam.print_for_row(text="TEXT 2", row=i)
    fam.print_for_row(text="TEXT 3", row=i)

fam.print_newlines(n=2)

for i in range(1,10):
    first_row_bg_color = "#FFDDDD"   # light red
    second_row_bg_color = "#DDDDFF"  # light blue

    fam.print_for_row(
        text="<important>TEXT A</important>",
        row=i,
        first_row_bg_color=first_row_bg_color,
        second_row_bg_color=second_row_bg_color # light blue
    )
    fam.print_for_row(
        text="<warning>TEXT B</warning>",
        row=i,
        first_row_bg_color=first_row_bg_color, # light red
        second_row_bg_color=second_row_bg_color # light blue
    )
    fam.print_for_row(
        text="TEXT C",
        row=i,
        first_row_bg_color=first_row_bg_color, # light red
        second_row_bg_color=second_row_bg_color # light blue
    )

    fam.print_newlines(n=1)