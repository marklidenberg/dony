from dony.parse_unknown_args import parse_unknown_args

if __name__ == "__main__":
    import sys

    print('sys.argv', sys.argv)

    print(parse_unknown_args(sys.argv))
