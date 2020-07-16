from typing import (
    Dict,
    List,
    Optional
)

import ansimarkup

class FancyAnsiMarkup:
    __am: ansimarkup.AnsiMarkup
    __tag_open: str
    __tag_close: str
    __default_line_length: int
    __default_first_row_bg_color: str
    __default_second_row_bg_color: str

    def __init__(
            self,
            tags: Dict[str, str] = None,
            always_reset: bool = False,
            strict: bool = True,
            tag_sep: str = '<>',
            ansistring_cls: type = None,
            default_line_length: int = 120,
            default_first_row_bg_color: str = "#fbfbfb",
            default_second_row_bg_color: str = "#f5f5f5"
    ) -> None:
        self.__tag_open = tag_sep[0]
        self.__tag_close = tag_sep[1]

        self.__default_first_row_bg_color = default_first_row_bg_color
        self.__default_second_row_bg_color = default_second_row_bg_color
        self.__default_line_length = default_line_length

        self.__am = ansimarkup.AnsiMarkup(
            tags=tags,
            always_reset=always_reset,
            strict=strict,
            tag_sep=tag_sep,
            ansistring_cls=ansistring_cls
        )

    def print_for_row(
            self,
            text: str,
            row: int,
            flush: bool = True,
            newline_at_end: bool = True,
            fill_with_spaces: bool = True,
            line_length: Optional[int] = None,
            first_row_bg_color: Optional[str] = None,
            second_row_bg_color: Optional[str] = None,
            *args: any,
            **kwargs: any
    ) -> None:
        # every second line is gray
        if row % 2 == 1:
            if first_row_bg_color is None:
                bg_color: str = self.__default_first_row_bg_color
            else:
                bg_color: str = first_row_bg_color
        else:
            if second_row_bg_color is None:
                bg_color: str = self.__default_second_row_bg_color
            else:
                bg_color: str = second_row_bg_color

        # print with filling spaces (optional), colors and new line at the end (optional)
        self.print_with_spaces(
            text=text,
            bg_color=bg_color,
            fill_with_spaces=fill_with_spaces,
            line_length=line_length,
            newline_at_end=newline_at_end,
            flush=flush,
            *args,
            **kwargs
        )

    def print_with_spaces(
            self,
            text: str,
            bg_color: Optional[str] = None,
            fill_with_spaces: bool = True,
            line_length: Optional[int] = None,
            flush: bool = True,
            newline_at_end: bool = True,
            *args: any,
            **kwargs: any
    ) -> None:
        if line_length is None:
            line_length = self.__default_line_length

        # fill end with spaces for continous background
        len_text: int = len(self.__am.strip(text))
        len_fill: int = line_length - len_text
        str_fill: str = ""
        if fill_with_spaces and len_fill > 0:
            for i in range(1, len_fill):
                str_fill += " "

        text += str_fill

        # add bg_color if not none
        if bg_color is not None:
            text = self.__bg_color_name_or_hex_start_tag(bg_color) + \
                   text + \
                   self.__bg_color_name_or_hex_end_tag(bg_color)

        # print with colors and new line at the end (optional)
        self.print_with_colors(
            text=text,
            flush=flush,
            newline_at_end=newline_at_end,
            *args,
            **kwargs
        )

    def print_newlines(self, n: int = 1):
        for i in range(1, n):
            self.__am.ansiprint("\n", end='')

    def print_with_colors(
            self,
            text: str = "",
            flush: bool = True,
            newline_at_end: bool = True,
            *args: any,
            **kwargs
    ) -> None:
        if newline_at_end:
            self.__am.ansiprint(
                text,
                flush=flush,
                *args,
                **kwargs
            )
        else:
            self.__am.ansiprint(
                text,
                flush=flush,
                end='',
                *args,
                **kwargs
            )

    def wrap_tag(self, text: str, tag: str):
        return  self.__tag_open + tag + self.__tag_close + \
                text + \
                self.__tag_open + "/" + tag + self.__tag_close


    def __bg_color_name_or_hex_start_tag(self, bg_color: str) -> str:
        if bg_color.startswith("#"):
            return  self.__tag_open + "bg " + bg_color + self.__tag_close
        else:
            return self.__tag_open + bg_color + self.__tag_close

    def __bg_color_name_or_hex_end_tag(self, bg_color: str) -> str:
        if bg_color.startswith("#"):
            return self.__tag_open + "/bg " + bg_color + self.__tag_close
        else:
            return self.__tag_open + "/" + bg_color + self.__tag_close