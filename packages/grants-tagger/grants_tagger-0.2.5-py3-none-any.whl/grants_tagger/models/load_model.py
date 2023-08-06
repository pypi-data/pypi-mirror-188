from grants_tagger.utils import save_pickle, load_pickle
from grants_tagger.models.mesh_xlinear import MeshXLinear


def load_model(approach, model_path, parameters=None):
    if str(model_path).endswith(".pkl"):
        model = load_pickle(model_path)
    else:
        model = MeshXLinear()
        model.load(model_path)

    if parameters:
        params = ast.literal_eval(parameters)
        model.set_params(**params)
    else:
        parameters = {}

    return model
