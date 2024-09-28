from pathlib import Path
from openai import OpenAI
import re


def extract_keys_from_template(template: str) -> list:
    return re.findall(r'{(.*?)}', template)


def replace_placeholder(template: str, placeholders: dict) -> str:
    pass


class PathUtils:
    _SRC = Path(__file__).resolve().parent.parent.parent
    _MAIN = _SRC / 'main'
    RESOURCES = _SRC / 'resources'
    DATA = RESOURCES / 'data'
    OUTPUT = RESOURCES / 'output_data'
    PROMPTS = RESOURCES / 'prompts'
    ENV_FILE = _SRC.parent / ".env"


class LLMModels:
    gpt_4 = "gpt-4"
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    o1_preview = "o1-preview"


class LLMPrompts:
    tags_extractor = PathUtils.PROMPTS / 'tags_extractor.txt'
    translate = PathUtils.PROMPTS / 'translate.txt'
    identify_language = PathUtils.PROMPTS / 'identify_language.txt'


class LLMUtils:
    @staticmethod
    def let_openai_to_work(prompt: str, message: str, model_name=LLMModels.gpt_4o_mini, **kwargs) -> str:
        if kwargs and len(kwargs) > 1:
            required_keys = extract_keys_from_template(prompt)
            missing_keys = [key for key in required_keys if key not in kwargs]
            if missing_keys:
                raise ValueError(f"Missing required keys: {missing_keys}")
        prompt = prompt.format(**kwargs)
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"Message: {message}"
                }
            ],
            temperature=0
        )
        return response.choices[0].message.content

    @staticmethod
    def extract_tags_from_message(message: str, model_name=LLMModels.gpt_4o_mini) -> list:
        prompt = LLMPrompts.tags_extractor.read_text()
        return LLMUtils.let_openai_to_work(prompt, message, model_name=model_name).split(",")

    @staticmethod
    def translate_text(message: str, model_name=LLMModels.gpt_4o_mini, **kwargs) -> str:
        if not kwargs or len(kwargs) == 0 or "input_lang" not in kwargs:
            raise ValueError(f"Missing required keys: input_lang")
        if "output_lang" not in kwargs:
            kwargs["output_lang"] = "English"
        prompt = LLMPrompts.translate.read_text()
        return LLMUtils.let_openai_to_work(prompt, message, model_name=model_name, **kwargs)

    @staticmethod
    def identify_language(message: str, model_name=LLMModels.gpt_4o_mini) -> str:
        prompt = LLMPrompts.identify_language.read_text()
        return LLMUtils.let_openai_to_work(prompt, message, model_name=model_name)
