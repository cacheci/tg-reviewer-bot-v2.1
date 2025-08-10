import os, json, re

config_dir = "/etc/tg_reviewer_bot_2/config.json"

# tg-reviewer-bot-v2.1

try:
    with open(config_dir, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Read config file, JSON config file mode.")

        # required settings
        if data['required'] is None:
            raise ValueError("Config file incorrect: \"required\" is missing.")

        TG_TOKEN                    = data['required']['TG_TOKEN']
        if TG_TOKEN is None:
            raise ValueError("Config file incorrect: \"TG_TOKEN\" is missing.")
        if re.fullmatch(r'^\d{6,}:[a-zA-Z0-9_]{35}$', TG_TOKEN):
            raise ValueError("Config file incorrect: \"TG_TOKEN\" is not correct token.")

        TG_REVIEWER_GROUP           = str(int(data['required']['TG_REVIEWER_GROUP']))
        if not TG_REVIEWER_GROUP:
            raise ValueError("Config file incorrect: \"TG_REVIEWER_GROUP\" is incorrect.")

        TG_PUBLISH_CHANNEL_JSON     = data['required']['TG_PUBLISH_CHANNEL']
        if TG_PUBLISH_CHANNEL_JSON is None:
            raise ValueError("Config file incorrect: \"TG_PUBLISH_CHANNEL\" missing.")
        if not isinstance(TG_PUBLISH_CHANNEL_JSON, list):
            raise ValueError("Config file incorrect: \"TG_PUBLISH_CHANNEL\" is incorrect.")
        if len(TG_PUBLISH_CHANNEL_JSON) == 0:
            raise ValueError("Config file incorrect: \"TG_PUBLISH_CHANNEL\" required at least one content.")
        TG_PUBLISH_CHANNEL          = str(int(":".join(TG_PUBLISH_CHANNEL_JSON)))

        TG_BOT_USERNAME             = data['required']['TG_BOT_USERNAME']
        if TG_BOT_USERNAME is None:
            raise ValueError("Config file incorrect: \"TG_BOT_USERNAME\" is missing.")
        if not TG_BOT_USERNAME.startswith("@"):
            raise ValueError("Config file incorrect: \"TG_BOT_USERNAME\" is incorrect.")

        # non-required settings
        TG_SINGLE_MODE              = data.get('non_required', {}).get('TG_SINGLE_MODE', True)
        if not isinstance(TG_SINGLE_MODE, bool):
            raise ValueError(f"Config file incorrect: \"TG_SINGLE_MODE\" is incorrect.")

        TG_TEXT_SPOILER             = data.get('non_required', {}).get('TG_TEXT_SPOILER', True)
        if not isinstance(TG_TEXT_SPOILER, bool):
            raise ValueError(f"Config file incorrect: \"TG_TEXT_SPOILER\" is incorrect.")

        TG_SELF_APPROVE             = data.get('non_required', {}).get('TG_SELF_APPROVE', True)
        if not isinstance(TG_SELF_APPROVE, bool):
            raise ValueError(f"Config file incorrect: \"TG_SELF_APPROVE\" is incorrect.")

        TG_RETRACT_NOTIFY           = data.get('non_required', {}).get('TG_RETRACT_NOTIFY', True)
        if not isinstance(TG_RETRACT_NOTIFY, bool):
            raise ValueError(f"Config file incorrect: \"TG_RETRACT_NOTIFY\" is incorrect.")

        TG_BANNED_NOTIFY            = data.get('non_required', {}).get('TG_BANNED_NOTIFY', True)
        if not isinstance(TG_BANNED_NOTIFY, bool):
            raise ValueError(f"Config file incorrect: \"TG_BANNED_NOTIFY\" is incorrect.")

        TG_REJECT_REASON_USER_LIMIT = data.get('non_required', {}).get('TG_REJECT_REASON_USER_LIMIT', True)
        if not isinstance(TG_REJECT_REASON_USER_LIMIT, bool):
            raise ValueError(f"Config file incorrect: \"TG_REJECT_REASON_USER_LIMIT\" is incorrect.")

        TG_REVIEWONLY               = data.get('non_required', {}).get('TG_REVIEWONLY', False)
        if not isinstance(TG_REVIEWONLY, bool):
            raise ValueError(f"Config file incorrect: \"TG_REVIEWONLY\" is incorrect.")

        APPROVE_NUMBER_REQUIRED     = int(str(data.get('non_required', {}).get('APPROVE_NUMBER_REQUIRED', 2)))

        REJECT_NUMBER_REQUIRED      = int(str(data.get('non_required', {}).get('REJECT_NUMBER_REQUIRED', 2)))

        TG_EXPAND_LENGTH            = int(str(data.get('non_required', {}).get('TG_EXPAND_LENGTH', 200)))

        TG_REJECTED_CHANNEL         = data.get('non_required', {}).get('TG_REJECTED_CHANNEL', None)
        if not isinstance(TG_REJECTED_CHANNEL, str):
            raise ValueError(f"Config file incorrect: \"TG_REJECTED_CHANNEL\" is incorrect.")

        REJECTION_REASON_JSON       = data.get('non_required', {}).get("TG_REJECTION_REASON", ["已有其他相似投稿","内容不够有趣","内容过于火星","引起感官不适","内容 NSFW","没有 Get 到梗","不在可接受范围内","点错了，正在召唤补发"])
        if not isinstance(REJECTION_REASON_JSON, list):
            raise ValueError("Config file incorrect: \"TG_PUBLISH_CHANNEL\" is incorrect.")
        if len(REJECTION_REASON_JSON) == 0:
            raise ValueError("Config file incorrect: \"REJECTION_REASON_JSON\" exist but have no content.")
        REJECTION_REASON            = ":".join(REJECTION_REASON_JSON)

        TG_DB_URL                   = data.get('non_required', {}).get('TG_DB_URL', "sqlite:///data/database.db")
        if not isinstance(TG_DB_URLL, str):
            raise ValueError(f"Config file incorrect: \"TG_DB_URL\" is incorrect.")

        TG_CUSTOMAPI                   = data.get('non_required', {}).get('TG_CUSTOMAPI', "https://api.telegram.org/bot")
        if not isinstance(TG_CUSTOMAPI, str):
            raise ValueError(f"Config file incorrect: \"TG_CUSTOMAPI\" is incorrect.")

except (json.JSONDecodeError) as e:
    raise EnvironmentError("Warning: Config JSON found decode failed!")
except (PermissionError) as e:
    raise EnvironmentError("Warning: Failed to read JSON file permission denied!")
except (FileNotFoundError) as e:
    print(f"Warning: Failed to read config file ({e}), trying environment variable...")

    # get args from environment virables
    # required settings
    TG_TOKEN                        = os.environ["TG_TOKEN"]

    TG_REVIEWER_GROUP               = os.environ["TG_REVIEWER_GROUP"]

    try:
        getenvkey                   = os.environ["TG_PUBLISH_CHANNEL"]
        if getenvkey is None:
            raise ValueError("Environment variable 'TG_PUBLISH_CHANNEL' not found!")
        TG_PUBLISH_CHANNEL          = getenvkey.split(":")
    except KeyError:
        raise ValueError("Environment variable 'TG_PUBLISH_CHANNEL' not found!")

    TG_BOT_USERNAME                 = os.environ["TG_BOT_USERNAME"]

    # non-required settings
    # bool
    TG_SINGLE_MODE                  = os.getenv("TG_SINGLE_MODE", "True")       == "True"

    TG_TEXT_SPOILER                 = os.getenv("TG_TEXT_SPOILER", "True")      == "True"

    TG_SELF_APPROVE                 = os.getenv("TG_SELF_APPROVE", "True")      == "True"

    TG_RETRACT_NOTIFY               = os.getenv("TG_RETRACT_NOTIFY", "True")    == "True"

    TG_BANNED_NOTIFY                = os.getenv("TG_BANNED_NOTIFY", "True")     == "True"

    TG_REJECT_REASON_USER_LIMIT     = os.getenv("TG_REJECT_REASON_USER_LIMIT", "True") == "True"

    TG_REVIEWONLY                   = os.getenv("TG_REVIEWONLY", "False")       == "True"

    # int
    try:
        APPROVE_NUMBER_REQUIRED     = int(os.getenv("TG_APPROVE_NUMBER_REQUIRED", 2))
    except (TypeError, ValueError):
        APPROVE_NUMBER_REQUIRED     = 2

    try:
        REJECT_NUMBER_REQUIRED      = int(os.getenv("TG_REJECT_NUMBER_REQUIRED", 2))
    except (TypeError, ValueError):
        REJECT_NUMBER_REQUIRED      = 2

    try:
        TG_EXPAND_LENGTH            = int(os.getenv("TG_EXPAND_LENGTH", 200))
    except (TypeError, ValueError):
        TG_EXPAND_LENGTH            = 200

    # string
    TG_REJECTED_CHANNEL             = os.environ.get("TG_REJECTED_CHANNEL")

    REJECTION_REASON                = os.environ.get("TG_REJECTION_REASON", "已有其他相似投稿:内容不够有趣:内容过于火星:引起感官不适:内容 NSFW:没有 Get 到梗:不在可接受范围内:点错了，正在召唤补发").split(":")

    TG_DB_URL                       = os.environ.get("TG_DB_URL", "sqlite:///data/database.db")

    TG_CUSTOMAPI                    = os.environ.get("TG_CUSTOMAPI", "https://api.telegram.org/bot")
