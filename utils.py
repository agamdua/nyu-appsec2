import subprocess
import tempfile


def run_spell_check(data):
    """
    Returns result of the spell check

    Args:
        data (string): text blurb to spell check
    """
    if data is None:
        return

    tmp_data_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_data_file.write(data)

    out = subprocess.run(
        ["./a.out", "wordlist.txt", tmp_data_file.name], stdout=subprocess.PIPE
    )
    return out
