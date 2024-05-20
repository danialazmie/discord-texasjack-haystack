from . import prompts

from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.builders import DynamicPromptBuilder

class TexasJack:

    def __init__(self):

        self.prompt_builder = DynamicPromptBuilder()
        self.model = OpenAIChatGenerator(
            model='gpt-3.5-turbo',
            generation_kwargs={'temperature': 0.9}
        )

        self.memory = [
            ChatMessage.from_system(prompts.CONTEXT_CHAT)
        ]

    def parse_discord_message(self, user: str, query: str) -> ChatMessage:

        parsed_prompt = self.prompt_builder.run(
            prompt_source=prompts.TEMPLATE_DISCORD_CHAT,
            template_variables={
                'user': user,
                'query': query
            }
        )

        return ChatMessage.from_user(parsed_prompt['prompt'])


    def prompt(self, user: str, query: str, context: str = 'chat') -> str:

        context_map = {
            'chat': prompts.CONTEXT_CHAT,
            'warn_vulgar': prompts.CONTEXT_WARN_VULGAR
        }
        if context not in context_map:
            raise ValueError(f'Unsupported context. Must be one of {list(context_map.keys())}')

        memory_template = [
            ChatMessage.from_system(context_map[context])
        ]

        user_prompt = self.parse_discord_message(user, query)
        memory_template.append(user_prompt)

        response = self.model.run(messages=memory_template)
        response_str = response['replies'][0].content

        return response_str
    
    def chat_with_memory(self, user: str, query: str) -> str:

        user_prompt = self.parse_discord_message(user, query)
        self.memory.append(user_prompt)

        response = self.model.run(messages=self.memory)
        self.memory.append(response['replies'][0])

        response_str = response['replies'][0].content

        return response_str
