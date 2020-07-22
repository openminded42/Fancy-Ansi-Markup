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
            always_reset: bool = True,
            strict: bool = True,
            tag_sep: str = '<>',
            ansistring_cls: type = None,
            default_line_length: int = 120,
            default_first_row_bg_color: str = "#E5E5E5",
            default_second_row_bg_color: str = "#D5D5D5"
    ) -> None:
        """
        Constructur
        :param tags: List of named tags as dictionary
        :param always_reset: Reset every markup at the end of a single print command
        :param strict: Within a print command, every opening tags needs a corresponding closing tag
        :param tag_sep: Seperator of tags, e.g. "{}" if you want print_with_colors(text="{red}Hello World{/red}") to
        print a red text.
        :param ansistring_cls: A class for ansistring
        :param default_line_length: Default maximal line length for printing a line with background color. Every line
        has the background color defined by print_with_bg_color(...) or print_for_row(...) up to the specified line
        length. Can be overwritten by a parameter of the aformentioned methods.
        :param default_first_row_bg_color: A default background-color for the i-th block of rows printed by
        method print_for_row(...). Default is a light grey. A color name (red, green, blue, ...) or hex-value,
        e.g. #00AAFF
        :param default_second_row_bg_color: A default background-color for the (i+1)-th block of rows printed by
        method print_for_rows(...). Default is a light grey being a bit darker than default_first_row_bg_color.
        A color name (red, green, blue, ...) or hex-value, e.g. #00AAFF
        """
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
        """

        :param text: The text to print
        :param row: The number of the current block of rows 1, 2, 3, 4, ...
        :param flush: Flush the text immediately to stdout
        :param newline_at_end: Whether to have a "\n" at the end
        :param fill_with_spaces: Whether to fill the lines with spaces such that the background is filled up to line
        length line_length
        :param line_length: The maximum line length to fill with background color (default value 120)
        :param first_row_bg_color: The background color of the first block of rows (lighter gray by default)
        :param second_row_bg_color: The background color of the second black of rows (light gray by default)
        :param args: Any args passed to ansiprint
        :param kwargs: Any kwargs passed to ansiprint
        :return:
        """
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
        self.print_with_bg_color(
            text=text,
            bg_color=bg_color,
            fill_with_spaces=fill_with_spaces,
            line_length=line_length,
            newline_at_end=newline_at_end,
            flush=flush,
            *args,
            **kwargs
        )

    def print_with_bg_color(
            self,
            text: str,
            bg_color: str,
            fill_with_spaces: bool = True,
            line_length: Optional[int] = None,
            flush: bool = True,
            newline_at_end: bool = True,
            *args: any,
            **kwargs: any
    ) -> None:
        """
        Print a line with specified background color and line length line_length. The line is filled with spaces up to
        line length line_length. The default line length is 120.
        :param text: The text to print
        :param bg_color: The background color
        :param fill_with_spaces: Fill with spaces up to line length line_length
        :param line_length: The line length that has the specified background color
        :param flush: Flush the text immediately to stdout
        :param newline_at_end: Whether to have a "\n" at the end
        :param args: Any args passed to ansiprint
        :param kwargs: Any kwargs passed to ansiprint
        :return:
        """
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

    def print_newlines(self, n: int = 1) -> None:
        """
        Print n new lines
        :param n: Number of new files to print
        """
        for i in range(0, n):
            self.__am.ansiprint("\n", end='')

    def print_with_colors(
            self,
            text: str = "",
            flush: bool = True,
            newline_at_end: bool = True,
            *args: any,
            **kwargs
    ) -> None:
        """
        :param text: Text to print
        :param flush: Flush the text immediately to stdout
        :param newline_at_end: Whether to have a "\n" at the end
        :param args: Any args passed to ansiprint
        :param kwargs: Any kwargs passed to ansiprint
        :return:
        """
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

    def wrap_tag(self, text: str, tag: str) -> str:
        """
        Wrap a tag around some text
        :param text: Thext
        :param tag: Tag to wrap
        :return: <tag>text</tag>
        """
        return self.__tag_open + tag + self.__tag_close +\
               text +\
               self.__tag_open + "/" + tag + self.__tag_close


    def __bg_color_name_or_hex_start_tag(self, bg_color: str) -> str:
        """
        Parse a color name (red, green, blue, ...) to tag <bg red>.
        Parse a hex-value like #AAFF00 to <bg #AAFF00>
        :param bg_color: background color
        :return: <bg_color> if bg_color is a color name or <bg bg_color> if it is a hex-value
        """
        return self.__tag_open + "bg " + bg_color + self.__tag_close

    def __bg_color_name_or_hex_end_tag(self, bg_color: str) -> str:
        """
        Parse a color name (red, green, blue, ...) to tag </bg red>.
        Parse a hex-value like #AAFF00 to </bg #AAFF00>
        :param bg_color: background color
        :return: </bg_color> if bg_color is a color name or </bg bg_color> if it is a hex-value
        """
        return self.__tag_open + "/bg " + bg_color + self.__tag_close