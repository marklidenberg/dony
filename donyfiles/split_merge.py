from marklidenberg_donyfiles import split_merge
import dony

if __name__ == "__main__":
    dony.command(run_from="git_root")(split_merge)()
