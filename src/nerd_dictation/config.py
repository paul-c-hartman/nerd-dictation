from platformdirs import PlatformDirs

class Config:
    def __init__(self):
        self.dirs = PlatformDirs("nerd-dictation", "paul-c-hartman", ensure_exists=True)
        self.temp_cookie_name = "nerd_dictation.cookie"
        self.simulate_input_code_command = -1

settings = Config()
