from marklidenberg_donyfiles import update_secrets_baseline
import dony

if __name__ == "__main__":
    dony.command(run_from="git_root")(update_secrets_baseline)()
