# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/06_vision_utils.ipynb.

# %% auto 0
__all__ = ['store_variables', 'load_variables']

# %% ../nbs/06_vision_utils.ipynb 1
import pickle

# %% ../nbs/06_vision_utils.ipynb 3
def store_variables(pkl_fn:str, # Filename of the pickle file
                    var_vals:list # A list of variable values
                   ) -> None:
    '''Save variable values in a pickle file.'''

    with open(pkl_fn, 'wb') as f:
        pickle.dump(var_vals, f)

# %% ../nbs/06_vision_utils.ipynb 4
def load_variables(pkl_fn # Filename of the pickle file
                  ):
    '''Load stored variable values from a pickle file.

    Returns: A list of variable values.
    '''

    with open(pkl_fn, 'rb') as f:
        return pickle.load(f)
