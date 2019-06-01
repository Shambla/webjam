import slackwatch
from pyfiglet import Figlet


def print_welcome():
    custom_fig = Figlet(font='caligraphy')
    print(custom_fig.renderText('webjam'))
    print("=" * 37 + " 1.0 " + "=" * 37 + "\n")
    print(" " * 10 + "Hope you don't want socks, cuz they about to get rocked off\n\n")


def main():
    print_welcome()
    slackwatch.init()


if __name__ == '__main__':
    main()
