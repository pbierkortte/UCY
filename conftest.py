# Tests validate against measured equinoxes, so default to accurate mode.
import os

os.environ.setdefault("UCY_FAST", "0")
