import argparse
from typing import List, Optional
from nerd_dictation import main_begin, main_end, main_cancel, main_suspend
from nerd_dictation.download_model import main as download_model, MODELS, DEFAULT_MODEL


def argparse_generic_command_cookie(subparse: argparse.ArgumentParser) -> None:
    subparse.add_argument(
        "--cookie",
        dest="path_to_cookie",
        default="",
        type=str,
        metavar="FILE_PATH",
        help="Location for writing a temporary cookie (this file is monitored to begin/end dictation).",
        required=False,
    )


def argparse_create_begin(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "begin",
        help="Begin dictation.",
        description=(
            "This creates the directory used to store internal data, "
            "so other commands such as sync can be performed."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_generic_command_cookie(subparse)

    subparse.add_argument(
        "--config",
        default=None,
        dest="config",
        type=str,
        metavar="FILE",
        help=(
            "Override the file used for the user configuration.\n"
            "Use an empty string to prevent the users configuration being read."
        ),
        required=False,
    )

    subparse.add_argument(
        "--vosk-model-dir",
        default="",
        dest="vosk_model_dir",
        type=str,
        metavar="DIR",
        help=("Path to the VOSK model, see: https://alphacephei.com/vosk/models"),
        required=False,
    )

    subparse.add_argument(
        "--vosk-grammar-file",
        default=None,
        dest="vosk_grammar_file",
        type=str,
        metavar="DIR",
        help=(
            "Path to a JSON grammar file.  This restricts the phrases recognized by VOSK for\n"
            "better accuracy.  See `vosk_recognizer_new_grm` in the API reference:\n"
            "https://github.com/alphacep/vosk-api/blob/master/src/vosk_api.h"
        ),
        required=False,
    )

    subparse.add_argument(
        "--pulse-device-name",
        dest="pulse_device_name",
        default="",
        type=str,
        metavar="IDENTIFIER",
        help=(
            "The name of the pulse-audio device to use for recording.\n"
            'See the output of "pactl list sources" to find device names (using the identifier following "Name:").'
        ),
        required=False,
    )

    subparse.add_argument(
        "--sample-rate",
        dest="sample_rate",
        default=44100,
        type=int,
        metavar="HZ",
        help=("The sample rate to use for recording (in Hz).\n" "Defaults to 44100."),
        required=False,
    )

    subparse.add_argument(
        "--defer-output",
        dest="defer_output",
        default=False,
        action="store_true",
        help=(
            "When enabled, output is deferred until exiting.\n"
            "\n"
            "This prevents text being typed during speech (implied with ``--output=STDOUT``)"
        ),
        required=False,
    )

    subparse.add_argument(
        "--continuous",
        dest="progressive_continuous",
        default=False,
        action="store_true",
        help=(
            "Enable this option, when you intend to keep the dictation process enabled for extended periods of time.\n"
            "without this enabled, the entirety of this dictation session will be processed on every update.\n"
            "Only used when ``--defer-output`` is disabled."
        ),
        required=False,
    )

    subparse.add_argument(
        "--timeout",
        dest="timeout",
        default=0.0,
        type=float,
        metavar="SECONDS",
        help=(
            "Time out recording when no speech is processed for the time in seconds.\n"
            "This can be used to avoid having to explicitly exit "
            "(zero disables)."
        ),
        required=False,
    )

    subparse.add_argument(
        "--idle-time",
        dest="idle_time",
        default=0.1,
        type=float,
        metavar="SECONDS",
        help=(
            "Time to idle between processing audio from the recording.\n"
            "Setting to zero is the most responsive at the cost of high CPU usage.\n"
            "The default value is 0.1 (processing 10 times a second), which is quite responsive in practice\n"
            "(the maximum value is clamped to 0.5)"
        ),
        required=False,
    )

    subparse.add_argument(
        "--delay-exit",
        dest="delay_exit",
        default=0.0,
        type=float,
        metavar="SECONDS",
        help=(
            "The time to continue running after an end request.\n"
            'this can be useful so "push to talk" setups can be released while you finish speaking\n'
            "(zero disables)."
        ),
        required=False,
    )

    subparse.add_argument(
        "--suspend-on-start",
        dest="suspend_on_start",
        default=False,
        action="store_true",
        help=(
            "Start the process and immediately suspend.\n"
            "Intended for use when nerd-dictation is kept open\n"
            "where resume/suspend is used for dictation instead of begin/end."
        ),
        required=False,
    )

    subparse.add_argument(
        "--punctuate-from-previous-timeout",
        dest="punctuate_from_previous_timeout",
        default=0.0,
        type=float,
        metavar="SECONDS",
        help=(
            "The time-out in seconds for detecting the state of dictation from the previous recording,\n"
            "this can be useful so punctuation it is added before entering the dictation"
            "(zero disables)."
        ),
        required=False,
    )

    subparse.add_argument(
        "--full-sentence",
        dest="full_sentence",
        default=False,
        action="store_true",
        help=(
            "Capitalize the first character.\n"
            "This is also used to add either a comma or a full stop when dictation is performed under the\n"
            "``--punctuate-from-previous-timeout`` value."
        ),
        required=False,
    )

    subparse.add_argument(
        "--numbers-as-digits",
        dest="numbers_as_digits",
        default=False,
        action="store_true",
        help=("Convert numbers into digits instead of using whole words."),
        required=False,
    )

    subparse.add_argument(
        "--numbers-use-separator",
        dest="numbers_use_separator",
        default=False,
        action="store_true",
        help=("Use a comma separators for numbers."),
        required=False,
    )

    subparse.add_argument(
        "--numbers-min-value",
        dest="numbers_min_value",
        default=None,
        type=int,
        help=(
            "Minimum value for numbers to convert from whole words to digits.\n"
            'This provides for more formal writing and prevents terms like "no one"\n'
            'from being turned into "no 1".'
        ),
        required=False,
    )

    subparse.add_argument(
        "--numbers-no-suffix",
        dest="numbers_no_suffix",
        default=False,
        action="store_true",
        help=(
            "Suppress number suffixes when --numbers-as-digits is specified.\n"
            'For example, this will prevent "first" from becoming "1st".'
        ),
        required=False,
    )

    subparse.add_argument(
        "--input",
        dest="input_method",
        default="PAREC",
        type=str,
        metavar="INPUT_METHOD",
        choices=("PAREC", "SOX", "PW-CAT"),
        help=(
            "Specify input method to be used for audio recording. Valid methods: PAREC, SOX, PW-CAT.\n"
            "\n"
            "- ``PAREC`` (external command, default)\n"
            "  See --pulse-device-name option to use a specific pulse-audio device.\n"
            "- ``SOX`` (external command)\n"
            "  For help on setting up sox, see ``readme-sox.rst`` in the nerd-dictation repository.\n"
            "- ``PW-CAT`` (external command)\n"
        ),
        required=False,
    )

    subparse.add_argument(
        "--output",
        dest="output",
        default="SIMULATE_INPUT",
        choices=("SIMULATE_INPUT", "STDOUT"),
        metavar="OUTPUT_METHOD",
        help=(
            "Method used to at put the result of speech to text.\n"
            "\n"
            "- ``SIMULATE_INPUT`` simulate keystrokes (default).\n"
            "- ``STDOUT`` print the result to the standard output.\n"
            "  Be sure only to handle text from the standard output\n"
            "  as the standard error may be used for reporting any problems that occur.\n"
        ),
        required=False,
    )
    subparse.add_argument(
        "--simulate-input-tool",
        dest="simulate_input_tool",
        default="XDOTOOL",
        choices=("XDOTOOL", "DOTOOL", "DOTOOLC", "YDOTOOL", "WTYPE", "STDOUT"),
        metavar="SIMULATE_INPUT_TOOL",
        help=(
            "Program used to simulate keystrokes (default).\n"
            "\n"
            "- ``XDOTOOL`` Compatible with the X server only (default).\n"
            "- ``DOTOOL`` Compatible with all Linux distributions and Wayland.\n"
            "- ``DOTOOLC`` Same as DOTOOL but for use with the `dotoold` daemon.\n"
            "- ``YDOTOOL`` Compatible with all Linux distributions and Wayland but requires some setup.\n"
            "- ``WTYPE`` Compatible with Wayland.\n"
            "- ``STDOUT`` Bare stdout with Ctrl-H for backspaces.\n"
            "  For help on setting up ydotool, see ``readme-ydotool.rst`` in the nerd-dictation repository.\n"
        ),
        required=False,
    )

    subparse.add_argument(
        "--verbose",
        dest="verbose",
        default=0,
        type=int,
        help=(
            "Verbosity level, defaults to zero (no output except for errors)\n"
            "\n"
            "- Level 1: report top level actions (dictation started, suspended .. etc).\n"
            "- Level 2: report internal details (may be noisy)."
        ),
        required=False,
    )

    subparse.add_argument(
        "-",
        dest="rest",
        default=False,
        nargs=argparse.REMAINDER,
        help=(
            "End argument parsing.\n"
            "This can be used for user defined arguments which configuration scripts may read from the ``sys.argv``."
        ),
    )

    subparse.set_defaults(
        func=lambda args: main_begin(
            path_to_cookie=args.path_to_cookie,
            vosk_model_dir=args.vosk_model_dir,
            pulse_device_name=args.pulse_device_name,
            sample_rate=args.sample_rate,
            input_method=args.input_method,
            progressive=not (args.defer_output or args.output == "STDOUT"),
            progressive_continuous=args.progressive_continuous,
            full_sentence=args.full_sentence,
            numbers_as_digits=args.numbers_as_digits,
            numbers_use_separator=args.numbers_use_separator,
            numbers_min_value=args.numbers_min_value,
            numbers_no_suffix=args.numbers_no_suffix,
            timeout=args.timeout,
            idle_time=min(args.idle_time, 0.5),
            delay_exit=args.delay_exit,
            punctuate_from_previous_timeout=args.punctuate_from_previous_timeout,
            config_override=args.config,
            output=args.output,
            simulate_input_tool=args.simulate_input_tool,
            suspend_on_start=args.suspend_on_start,
            verbose=args.verbose,
            vosk_grammar_file=args.vosk_grammar_file,
        ),
    )


def argparse_create_end(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "end",
        help="End dictation.",
        description="""\
This ends dictation, causing the text to be typed in.
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_generic_command_cookie(subparse)

    subparse.set_defaults(
        func=lambda args: main_end(
            path_to_cookie=args.path_to_cookie,
        ),
    )


def argparse_create_cancel(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "cancel",
        help="Cancel dictation.",
        description="This cancels dictation.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_generic_command_cookie(subparse)

    subparse.set_defaults(
        func=lambda args: main_cancel(
            path_to_cookie=args.path_to_cookie,
        ),
    )


def argparse_create_suspend(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "suspend",
        help="Suspend the dictation process.",
        description=(
            "Suspend recording audio & the dictation process.\n"
            "\n"
            "This is useful on slower systems or when large language models take longer to load.\n"
            "Recording audio is stopped and the process is paused to remove any CPU overhead."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_generic_command_cookie(subparse)

    subparse.set_defaults(
        func=lambda args: main_suspend(
            path_to_cookie=args.path_to_cookie,
            suspend=True,
            verbose=1,
        ),
    )


def argparse_create_resume(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "resume",
        help="Resume the dictation process.",
        description=(
            "Resume recording audio & the dictation process.\n"
            "\n"
            "This is to be used to resume after the 'suspend' command.\n"
            "When nerd-dictation is not suspended, this does nothing.\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argparse_generic_command_cookie(subparse)

    subparse.set_defaults(
        func=lambda args: main_suspend(
            path_to_cookie=args.path_to_cookie,
            suspend=False,
            verbose=1,
        ),
    )


def argparse_create_download(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    subparse = subparsers.add_parser(
        "download",
        help="Download the VOSK model.",
        description=(
            "This is a helper command to download VOSK models.\n"
            "A model is required for dictation to work. Available models can be viewed at:\n"
            "https://alphacephei.com/vosk/models\n"
            "\n"
            "This simply downloads and extracts a model into the default location used by nerd-dictation,\n"
            "which is probably $XDG_CONFIG_DIR/nerd-dictation/model\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparse.add_argument(
        "--model",
        choices=MODELS.keys(),
        default=DEFAULT_MODEL,
        dest="model",
        type=str,
        help=(
            f"The name of the model to download. Defaults to '{DEFAULT_MODEL}'.\n"
            + "These can be found at: https://alphacephei.com/vosk/models.\n"
            + "To use a different model, use the URL to the model file as the argument, for example:\n"
            + " --model=\"https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip\"\n"
        ),
        required=False,
    )

    subparse.add_argument(
        "--force",
        dest="force",
        default=False,
        action="store_true",
        help=(
            "Force download and unzip the model even if one is already present.\n"
            "This can be useful if the model is corrupted or if you want to update to a newer version of the model.\n"
            "WARNING: will overwrite any existing model without confirmation. Use with caution!"
        ),
        required=False,
    )

    subparse.add_argument(
        "-y",
        dest="confirmation",
        default=False,
        action="store_true",
        help=(
            "Confirm overwriting an existing model.\n"
            "Use this flag to pass the interactive check if using --force."
        ),
        required=False,
    )

    subparse.set_defaults(
        func=lambda args: download_model(args.model, args.force, args.confirmation),
    )


def argparse_create() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    argparse_create_begin(subparsers)

    argparse_create_end(subparsers)
    argparse_create_cancel(subparsers)

    argparse_create_suspend(subparsers)
    argparse_create_resume(subparsers)

    argparse_create_download(subparsers)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse_create()
    args = parser.parse_args(argv)
    # Call sub-parser callback.
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)