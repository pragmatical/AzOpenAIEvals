import os
from typing import Any, Optional, Union

from evals.api import CompletionResult
from evals.base import CompletionFnSpec
from evals.prompt.base import ChatCompletionPrompt, OpenAICreateChatPrompt, Prompt
from evals.record import record_sampling
from evals.utils.api_utils import openai_chat_completion_create_retrying
from openai import AzureOpenAI


class AzureOpenAIBaseCompletionResult(CompletionResult):
    def __init__(self, raw_data: Any, prompt: Any):
        self.raw_data = raw_data
        self.prompt = prompt

    def get_completions(self) -> list[str]:
        raise NotImplementedError


class AzureOpenAIChatCompletionResult(AzureOpenAIBaseCompletionResult):
    def get_completions(self) -> list[str]:
        completions = []
        if self.raw_data:
            for choice in self.raw_data.choices:
                if choice.message.content is not None:
                    completions.append(choice.message.content)
        return completions


class AzureOpenAIChatCompletionFn(CompletionFnSpec):
    def __init__(
        self,
        n_ctx: Optional[int] = None,
        extra_options: Optional[dict] = {},
        **kwargs,
    ):
        self.model = os.environ.get("AZURE_OPENAI_MODEL")
        self.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
        self.n_ctx = n_ctx
        self.extra_options = extra_options

    def __call__(
        self,
        prompt: Union[str, OpenAICreateChatPrompt],
        **kwargs,
    ) -> AzureOpenAIChatCompletionResult:
        if not isinstance(prompt, Prompt):
            assert (
                isinstance(prompt, str)
                or (
                    isinstance(prompt, list)
                    and all(isinstance(token, int) for token in prompt)
                )
                or (
                    isinstance(prompt, list)
                    and all(isinstance(token, str) for token in prompt)
                )
                or (
                    isinstance(prompt, list)
                    and all(isinstance(msg, dict) for msg in prompt)
                )
            ), f"Got type {type(prompt)}, with val {type(prompt[0])} for prompt, expected str or list[int] or list[str] or list[dict[str, str]]"

            prompt = ChatCompletionPrompt(
                raw_prompt=prompt,
            )

        openai_create_prompt: OpenAICreateChatPrompt = prompt.to_formatted_prompt()

        client = AzureOpenAI(
            azure_endpoint=self.api_base,
            api_key=self.api_key,
            api_version=self.api_version,
        )

        result = openai_chat_completion_create_retrying(
            client,
            model=self.model,
            messages=openai_create_prompt,
            **{**kwargs, **self.extra_options},
        )
        result = AzureOpenAIChatCompletionResult(
            raw_data=result, prompt=openai_create_prompt
        )
        record_sampling(prompt=result.prompt, sampled=result.get_completions())
        return result
