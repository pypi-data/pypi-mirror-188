"""Wrapper around AI21 APIs."""
from typing import Any, Dict, List, Mapping, Optional

import requests
from pydantic import BaseModel, Extra, root_validator

from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env


class AI21PenaltyData(BaseModel):
    """Parameters for AI21 penalty data."""

    scale: int = 0
    applyToWhitespaces: bool = True
    applyToPunctuations: bool = True
    applyToNumbers: bool = True
    applyToStopwords: bool = True
    applyToEmojis: bool = True


class AI21(LLM, BaseModel):
    """Wrapper around AI21 large language models.

    To use, you should have the environment variable ``AI21_API_KEY``
    set with your API key.

    Example:
        .. code-block:: python

            from langchain import AI21
            ai21 = AI21(model="j1-jumbo")
    """

    model: str = "j1-jumbo"
    """Model name to use."""

    temperature: float = 0.7
    """What sampling temperature to use."""

    maxTokens: int = 256
    """The maximum number of tokens to generate in the completion."""

    minTokens: int = 0
    """The minimum number of tokens to generate in the completion."""

    topP: float = 1.0
    """Total probability mass of tokens to consider at each step."""

    presencePenalty: AI21PenaltyData = AI21PenaltyData()
    """Penalizes repeated tokens."""

    countPenalty: AI21PenaltyData = AI21PenaltyData()
    """Penalizes repeated tokens according to count."""

    frequencyPenalty: AI21PenaltyData = AI21PenaltyData()
    """Penalizes repeated tokens according to frequency."""

    numResults: int = 1
    """How many completions to generate for each prompt."""

    logitBias: Optional[Dict[str, float]] = None
    """Adjust the probability of specific tokens being generated."""

    ai21_api_key: Optional[str] = None

    base_url: Optional[str] = None
    """Base url to use, if None decides based on model name."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        ai21_api_key = get_from_dict_or_env(values, "ai21_api_key", "AI21_API_KEY")
        values["ai21_api_key"] = ai21_api_key
        return values

    @property
    def _default_params(self) -> Mapping[str, Any]:
        """Get the default parameters for calling AI21 API."""
        return {
            "temperature": self.temperature,
            "maxTokens": self.maxTokens,
            "minTokens": self.minTokens,
            "topP": self.topP,
            "presencePenalty": self.presencePenalty.dict(),
            "countPenalty": self.countPenalty.dict(),
            "frequencyPenalty": self.frequencyPenalty.dict(),
            "numResults": self.numResults,
            "logitBias": self.logitBias,
        }

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**{"model": self.model}, **self._default_params}

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "ai21"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call out to AI21's complete endpoint.

        Args:
            prompt: The prompt to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            The string generated by the model.

        Example:
            .. code-block:: python

                response = ai21("Tell me a joke.")
        """
        if stop is None:
            stop = []
        if self.base_url is not None:
            base_url = self.base_url
        else:
            if self.model in ("j1-grande-instruct",):
                base_url = "https://api.ai21.com/studio/v1/experimental"
            else:
                base_url = "https://api.ai21.com/studio/v1"
        response = requests.post(
            url=f"{base_url}/{self.model}/complete",
            headers={"Authorization": f"Bearer {self.ai21_api_key}"},
            json={"prompt": prompt, "stopSequences": stop, **self._default_params},
        )
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"AI21 /complete call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )
        response_json = response.json()
        return response_json["completions"][0]["data"]["text"]
