from logging import Logger


class IndexedChoiceSelector:
    """ Creates a dict from a list of options, or takes in an already enumerated dictionary.
    The aforementioned contains the options given enumerated into key value pairs.
    Then, Using SelectIndexedChoice, a choice can be made from that dictionary
    using either the key or the value itself.

    if a logger is not given, a dummy logger that does not save/show its output is used.
    """

    def __init__(self, title_of_list: str, logger: Logger = None, **kwargs):
        self.title_of_list = title_of_list
        self.logger = logger
        self.kwargs = kwargs

        if self.logger:
            pass
        else:
            self.logger = Logger('dummy_logger')

        if 'numbered_dict' not in self.kwargs:
            if 'options' in self.kwargs and isinstance(self.kwargs['options'], list):
                self.options = self.kwargs['options']
                self.numbered_dict = self._get_indexed_choices()
                self.validated = self._validate_numbered_dict()
            else:
                raise AttributeError("Either a numbered dict or a list of options must be provided.")
        else:
            if isinstance(self.kwargs['numbered_dict'], dict):
                self.numbered_dict = self.kwargs['numbered_dict']
                self.validated = self._validate_numbered_dict()
            else:
                try:
                    raise TypeError("The numbered_dict keyword argument must be a dictionary.")
                except TypeError as e:
                    self.logger.error(e, exc_info=True)
                    raise e

    def _validate_numbered_dict(self) -> bool:
        for n in self.numbered_dict:
            if isinstance(n, int) or n.isdigit():
                continue
            else:
                try:
                    raise ValueError("numbered dict keys must all be integers")
                except ValueError as e:
                    self.logger.error(e, exc_info=True)
                    raise e
        return True

    def _get_indexed_choices(self) -> dict:
        numbered_dict = dict(enumerate(self.options, start=1))
        return numbered_dict

    def _print_indexed_choices(self) -> None:
        print(f"\n{self.title_of_list} Options: ")
        for n, x in self.numbered_dict.items():
            print("\t" + str(n) + ". " + x)
        print("-------------------")

    def SelectIndexedChoice(self) -> str:
        if self.validated:
            self._print_indexed_choices()
            while True:
                try:
                    choice = input(f"Please choose a(n) {self.title_of_list}, or press q to quit: ").lower()
                except KeyboardInterrupt as e:
                    print("\nctrl-c detected, quitting!")
                    self.logger.warning("ctrl-c detected, quitting!")
                    exit(-1)

                # noinspection PyUnboundLocalVariable
                if choice.lower() == 'q':
                    print("Ok Quitting! Goodbye!")
                    self.logger.warning("Quitting due to user choice!")
                    exit(-1)

                elif choice in [x.lower() for x in self.numbered_dict.values()] or choice in [str(x) for x in self.numbered_dict]:
                    if choice.isdigit():
                        self.logger.debug("index detected, converting int to its real value")
                        choice = self.numbered_dict[int(choice)]
                        return choice
                    else:
                        return choice
                else:
                    print(choice)
                    print(f"your choice: \'{choice}\' was not valid!")
                    self.logger.warning(f"\'{choice}\' is not a valid choice! Retrying")
        else:
            try:
                raise ValueError("Either options must be provided or a VALID numbered_dict must be provided.")
            except ValueError as e:
                self.logger.error(e, exc_info=True)
