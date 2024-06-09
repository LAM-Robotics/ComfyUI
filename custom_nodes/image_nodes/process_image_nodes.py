import logging
from random import random
import base64
from easy_nodes import (
    NumberInput,
    ComfyNode,
    MaskTensor,
    StringInput,
    ImageTensor,
    Choice,
)
import easy_nodes
import torch
from typing import Union
from io import BytesIO


my_category = "LAM"

# By default EasyNodes will auto-register any decorated function (automatically insert it into ComfyUI's node registry).
# If you want to manually register your nodes the regular way, turn off
# auto_register and call easy_nodes.get_node_mappings()
easy_nodes.initialize_easy_nodes(default_category=my_category, auto_register=True)

# This is the converted example node from ComfyUI's example_node.py.example file.
@ComfyNode(my_category, is_output_node=True)
def encode_image_to_base64(image: Union[str, BytesIO, torch.Tensor]) -> str:
    print(f"Received input of type: {type(image)}")
    assert isinstance(image, (str, BytesIO, torch.Tensor)), f"Input must be a file path, a BytesIO object, or a torch.Tensor, got {type(image)}"

    if isinstance(image, str):
        with open(image, "rb") as image_file:
            image_data = image_file.read()
    elif isinstance(image, BytesIO):
        image_data = image.read()
    elif isinstance(image, torch.Tensor):
        # Assuming the tensor is an image in HWC format (Height, Width, Channels) with values in [0, 1]
        # Convert the tensor to a byte array
        image_data = (image * 255).byte().numpy().tobytes()
    else:
        raise ValueError("Unsupported input type")
    
    easy_nodes.show_text(f"hello: {str(base64.b64encode(image_data).decode('utf-8'))}")
    return base64.b64encode(image_data).decode('utf-8')