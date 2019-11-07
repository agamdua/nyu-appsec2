import subprocess


def run_spell_check(data):
    """
    Returns result of the spell check

    Args:
        data (string): text blurb to spell check
    """
    if data is None:
        return

    out = subprocess.run(["./a.out", data], stdout=subprocess.PIPE)
    return out
