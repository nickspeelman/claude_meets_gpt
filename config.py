import os

config = {
    "Claude": {
        "api_key": os.getenv("CLAUDE_API_KEY"),
        "api_endpoint": "https://api.anthropic.com/v1",
        "voice_id": "iP95p4xoKVk53GoZ742B",
        "elevenlabs_voice_name": "Chris",
        "models": {
            "default": "Claude Opus",
            "Claude Sonnet 3.5": {
                "model_id": "claude-3-5-sonnet-20240620",
                "max_tokens": 8192
            },
            "Claude Sonnet 2.0": {
                "model_id": "claude-2-0-sonnet",
                "max_tokens": 4096
            },
            "Claude Opus": {
                "model_id": "claude-3-opus-20240229",
                "max_tokens": 4096

            }
        }
    },
    "ChatGPT": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "api_endpoint": "https://api.openai.com/v1",
        "voice_id": "cgSgspJ2msm6clMCkdW9",
        "elevenlabs_voice_name": "Jessica",
        "models": {
            "default": "GPT-4o",
            "GPT-4 turbo": {
                "model_id": "gpt-4-turbo",
                "max_tokens": 4096
            },
            "GPT-3.5": {
                "model_id": "gpt-3.5-turbo",
                "max_tokens": 4096
            },
            "GPT-4": {
                "model_id": "gpt-4",
                "max_tokens": 8092
            },
            "GPT-4o": {
                "model_id": "gpt-4o",
                "max_tokens": 4096
            }
        }
    }
}




