from marklidenberg_donyfiles import release
import dony

if __name__ == "__main__":
    dony.command(run_from="git_root")(release)()
