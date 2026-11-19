"""
Karaoke-style lyrics: letters fill in one by one while the song plays.

    python lyrics_player.py          -> karaoke play
    python lyrics_player.py --sync   -> tap Enter at each line start to record exact timings
"""
import os
import sys
import time
import pygame

AUDIO_FILE = "song.mp3"

# Timestamps = line START time (seconds). Run --sync once for exact ones.
LYRICS = [
    (0.30, "Sachi si hain yeh taarifein"),
    (5.20, "Dil se jo maine kari hain"),
    (10.30, "Jo tu mila to saji hain"),
    (13.6, "duniya meri humdum"),
    (19.53, "O aasmaan mila zameen ko meri"),
    (24.41, "Aadhe aadhe poore hain hum"),
]

# ---- Karaoke tuning ----
GAP = 0.25            # line finishes this many sec before next line starts
LAST_LINE_TIME = 4.0  # how long the last line takes to fill
OFFSET = 0.0          # +ve = lyrics later, -ve = lyrics earlier (global shift)

# ---- Colors (ANSI) ----
SUNG = "\033[1;93m"    # bold bright yellow  (already sung)
UNSUNG = "\033[90m"    # dim grey            (yet to sing)
RESET = "\033[0m"
CLEAR_EOL = "\033[K"

os.system("")  # enables ANSI colors in Windows terminals


def load_audio():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(AUDIO_FILE)
    except pygame.error as e:
        print(f"Could not load '{AUDIO_FILE}': {e}")
        sys.exit(1)


def line_window(i):
    """(start, end) time in seconds for line i."""
    start = LYRICS[i][0] + OFFSET
    if i + 1 < len(LYRICS):
        end = LYRICS[i + 1][0] + OFFSET - GAP
    else:
        end = start + LAST_LINE_TIME
    return start, max(end, start + 0.2)


def render(text, n):
    """Redraw current line: first n chars highlighted, rest dim."""
    sys.stdout.write(f"\r{SUNG}{text[:n]}{UNSUNG}{text[n:]}{RESET}{CLEAR_EOL}")
    sys.stdout.flush()


def play():
    load_audio()
    pygame.mixer.music.play()
    current = -1
    try:
        while pygame.mixer.music.get_busy():
            elapsed = pygame.mixer.music.get_pos() / 1000.0

            # which line is active right now?
            idx = -1
            for i in range(len(LYRICS)):
                if LYRICS[i][0] + OFFSET <= elapsed:
                    idx = i

            # moved to a new line -> finish the previous one
            if idx != current:
                if current >= 0:
                    render(LYRICS[current][1], len(LYRICS[current][1]))
                    print()
                current = idx

            if current >= 0:
                text = LYRICS[current][1]
                start, end = line_window(current)
                progress = min(max((elapsed - start) / (end - start), 0.0), 1.0)
                render(text, int(progress * len(text)))

            time.sleep(0.02)

        # song ended -> finish last line
        if current >= 0:
            render(LYRICS[current][1], len(LYRICS[current][1]))
            print()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()


def sync():
    """Press Enter exactly when each line STARTS being sung."""
    load_audio()
    print("Get ready. Music starts right after you press Enter.")
    input("Press Enter to start...")
    pygame.mixer.music.play()

    recorded = []
    try:
        for _, line in LYRICS:
            print(f"\nNext line: {line}")
            input("   press Enter when it starts -> ")
            t = pygame.mixer.music.get_pos() / 1000.0
            recorded.append((round(t, 2), line))
            print(f"   saved {t:.2f}s")
    except KeyboardInterrupt:
        print("\nCancelled.")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    if recorded:
        print("\n\nPaste this over LYRICS in the script:\n")
        print("LYRICS = [")
        for t, line in recorded:
            print(f'    ({t}, "{line}"),')
        print("]")


if __name__ == "__main__":
    if "--sync" in sys.argv:
        sync()
    else:
        play()