import os, sys
import distutils.util

# https://stackoverflow.com/a/287944/3211506
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CLI():
    COLORS = bcolors
    GAP = f"\033[95m==>>>\033[0m "

    def __init__(self) -> None:
        pass

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_sep():
        print("======================")

    @staticmethod
    def presskeycont():
        input("Press Enter to continue...")
        return

    @staticmethod
    def getPositiveNonZeroFloat(question, default = None) -> float:

        prompt = f"[Default = {default}]" if default is not None else ""

        while True:
            try:
                resp = input(CLI.GAP + question + " " + prompt + " > ").strip()
                if default is not None and resp == '':
                    return default
                else:
                    resp = float(resp)
                    if resp <= 0: 
                        raise ValueError
                    return resp
            except ValueError:
                print("ERROR: Please respond with a positive number/float.")
            except EOFError:
                print("Encountered EOF, exiting...")
                sys.exit()

    @staticmethod
    def getIntWithLimit(question, default = None, lowerlimit: int = 1) -> int:
        """Gets an integer that is no lower than the `lowerlimit`

        Parameters
        ----------
        question : str
            Question to ask
        default : int, optional
            Default value, by default None
        lowerlimit : int, optional
            Lowest acceptable integer, by default 1

        Returns
        -------
        int
            Received input
        """

        prompt = f"[Default = {default}]" if default is not None else ""

        while True:
            try:
                resp = input(CLI.GAP + question + " " + prompt + " > ").strip()
                if default is not None and resp == '':
                    return default
                else:
                    resp = int(resp)
                    if resp <= lowerlimit: 
                        raise ValueError
                    return resp
            except ValueError:
                print(f"ERROR: Please respond with an integer that is at least {lowerlimit}")
            except EOFError:
                print("Encountered EOF, exiting...")
                sys.exit()

    @staticmethod
    def options(question, options, default):
        assert (default in options) or (default is None), "ERROR: default not in options"

        prompt = f"[Default = {default}]" if default is not None else ""

        while True:
            try:
                resp = input(CLI.GAP + question + " " + prompt + " > ").strip().lower()
                if default is not None and resp == '':
                    return default
                else:
                    if resp not in options:
                        raise ValueError
                    return resp
            except ValueError:
                print("ERROR: Please respond with one of the options.")
            except EOFError:
                print("Encountered EOF, exiting...")
                sys.exit()

    # https://gist.github.com/garrettdreyfus/8153571?permalink_comment_id=3263216#gistcomment-3263216
    @staticmethod
    def whats_it_gonna_be_boy(question, default='no') -> bool:
        if default is None:
            prompt = " [y/n]"
        elif default == 'yes':
            prompt = " [Y/n]"
        elif default == 'no':
            prompt = " [y/N]"
        else:
            raise ValueError(f"Unknown setting '{default}' for default.")

        while True:
            try:
                resp = input(CLI.GAP + question + prompt + " > ").strip().lower()
                if default is not None and resp == '':
                    return (default == 'yes')
                else:
                    return bool(distutils.util.strtobool(resp))
            except ValueError:
                print("ERROR: Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
            except EOFError:
                print("Encountered EOF, exiting...")
                sys.exit()