import requests
import datetime

class PromptLayerBase(object):
    __slots__ = ["_obj", "__weakref__", "_function_name", "_provider_type", "_identifying_params"]

    def __init__(self, obj, function_name="", provider_type="openai"):
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_function_name", function_name)
        object.__setattr__(self, "_provider_type", provider_type)
        if provider_type == "langchain":
            object.__setattr__(self, "_identifying_params", obj._identifying_params)
            object.__setattr__(self, "_function_name", f"langchain.{obj.__repr_name__()}")

    def __getattr__(self, name):
        return PromptLayer(
            getattr(object.__getattribute__(self, "_obj"), name),
            function_name=f'{object.__getattribute__(self, "_function_name")}.{name}',
            provider_type=object.__getattribute__(self, "_provider_type"),
        )

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_obj"), name, value)

    def __call__(self, *args, **kwargs):
        from promptlayer.utils import get_api_key
        tag = kwargs.pop("pl_tags", None)
        request_start_time = datetime.datetime.now().timestamp()
        response = object.__getattribute__(self, "_obj")(*args, **kwargs)
        request_end_time = datetime.datetime.now().timestamp()
        if object.__getattribute__(self, "_provider_type") == "langchain":
            kwargs = {**kwargs, **object.__getattribute__(self, "_identifying_params")}
        request_response = requests.post(
            "https://api.promptlayer.com/track-request",
            json={
                "function_name": object.__getattribute__(self, "_function_name"),
                "provider_type": object.__getattribute__(self, "_provider_type"),
                "args": args,
                "kwargs": kwargs,
                "tags": tag,
                "request_response": response,
                "request_start_time": request_start_time,
                "request_end_time": request_end_time,
                "api_key": get_api_key(),
            },
        )
        if request_response.status_code != 200:
            raise Exception(f"Error while tracking request: {request_response.json().get('message')}")
        return response
