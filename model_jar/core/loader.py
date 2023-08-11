import os
import sys
import torch


def load_from_dir(
    name: str,
    dir_path: str,
    checkpoint: str,
    checkpoint_key: str,
) -> torch.nn.Module:
    sys.path.append(dir_path)

    try:
        model_jar_module = __import__("model_jar")
        ModelClass       = getattr(model_jar_module, name)
        model_attributes = getattr(model_jar_module, 'default_attributes')

    except ImportError:
        raise ImportError("The model_jar is not found.")

    except AttributeError:
        available_names = [attr for attr in dir(model_jar_module) if not attr.startswith("_")]
        raise ValueError(f"The model class '{name}' was not found in hubconf.py. Available model classes: {available_names}")

    model = ModelClass(model_attributes[name])

    # Load the checkpoint
    checkpoint_path = os.path.join(dir_path, checkpoint)
    checkpoint_data = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(checkpoint_data[checkpoint_key])

    sys.path.remove(dir_path)

    return model
