from marklidenberg_donyfiles import updates_secrets_baseline
import dony

if __name__ == "__main__":
    dony.command(run_from="git_root")(updates_secrets_baseline)()
