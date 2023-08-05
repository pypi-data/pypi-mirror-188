# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_vision_core.ipynb.

# %% auto 0
__all__ = ['med_img_reader', 'MetaResolver', 'MedBase', 'MedImage', 'MedMask']

# %% ../nbs/01_vision_core.ipynb 2
from .vision_plot import *
from fastai.data.all import *
from torchio import ScalarImage, LabelMap, ToCanonical, Resample
import pickle
import warnings

# %% ../nbs/01_vision_core.ipynb 4
def _preprocess(o, reorder, resample):  
    
    if reorder:
        transform = ToCanonical()
        o = transform(o)
        
    org_size = o.shape[1:]
    
    if resample and not all(np.isclose(o.spacing, resample)):
            transform = Resample(resample)
            o = transform(o)
            
    if MedBase.affine_matrix is None:
        MedBase.affine_matrix = o.affine
            
    return o, org_size

# %% ../nbs/01_vision_core.ipynb 6
def _load(fn:(str, Path), dtype=None):
    '''Private method to load image as either ScalarImage or LabelMap.

    Args:
        fn : Image path.
        dtype: Datatype.

    Returns:
        (ScalarImage, LabelMap): An object that contains a 4D tensor and metadata.
    '''

    if dtype is MedMask: return LabelMap(fn)
    else: return ScalarImage(fn)

# %% ../nbs/01_vision_core.ipynb 7
def _multi_channel(img_fns:list, reorder:bool, resample:list, dtype):
    '''Private method to load multisequence data.

    Args:
        img_fns: List of image paths s(e.g. T1, T2, T1CE, DWI).

    Returns:
        torch.Tensor: A stacked 4D tensor.
    '''

    img_list = []
    for fn in img_fns:
        o = _load(fn, dtype=dtype)
        o,_ = _preprocess(o, reorder, resample)
        img_list.append(o.data[0])            

    return dtype(torch.stack(img_list, dim=0))

# %% ../nbs/01_vision_core.ipynb 8
def med_img_reader(fn:(str, Path), # Image path
                   dtype=torch.Tensor, # Datatype (MedImage, MedMask, torch.Tensor)
                   reorder:bool=False, # Whether to reorder the data to be closest to canonical (RAS+) orientation.
                   resample:list=None, # Whether to resample image to different voxel sizes and image dimensions.
                   only_tensor:bool=True # Whether to return only image tensor
                  ):
    '''Load and preprocess medical image'''
        
    if isinstance(fn, str) and ';' in fn:
        img_fns = fn.split(';')
        return _multi_channel(img_fns, reorder, resample, dtype=dtype)

    org_img = _load(fn, dtype=dtype)
    input_img, org_size = _preprocess(org_img, reorder, resample)

    if only_tensor: return dtype(input_img.data.type(torch.float))

    return org_img, input_img, org_size

# %% ../nbs/01_vision_core.ipynb 10
class MetaResolver(type(torch.Tensor), metaclass=BypassNewMeta):
    '''A class to bypass metaclass conflict:
    https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/data/batch.html
    '''

    pass

# %% ../nbs/01_vision_core.ipynb 11
class MedBase(torch.Tensor, metaclass=MetaResolver):
    '''A class that represents an image object. Metaclass casts x to this class if it is of type cls._bypass_type.'''

    _bypass_type=torch.Tensor
    _show_args = {'cmap':'gray'}
    resample, reorder = None, False
    affine_matrix = None

    @classmethod
    def create(cls, fn:(Path,str, torch.Tensor), **kwargs):
        '''Open an medical image and cast to MedBase object. If it is a torch.Tensor cast to MedBase object.

        Args:
            fn: Image path or a 4D torch.Tensor.
            kwargs: additional parameters.

        Returns:
            A 4D tensor as MedBase object.
        '''

        if isinstance(fn, torch.Tensor): return cls(fn)
        return med_img_reader(fn, dtype=cls, resample=cls.resample, reorder=cls.reorder)

    @classmethod
    def item_preprocessing(cls, resample:(list, int, tuple), reorder:bool):
        '''Change the values for the class variables `resample` and `reorder`.

        Args:
            resample: A list with voxel spacing.
            reorder: Wheter to reorder the data to be closest to canonical (RAS+) orientation.
        '''

        cls.resample = resample
        cls.reorder = reorder

    def show(self, ctx=None, channel=0, indices=None, anatomical_plane=0, **kwargs):
        "Show Medimage using `merge(self._show_args, kwargs)`"
        return show_med_img(self, ctx=ctx, channel=channel, indices=indices, anatomical_plane=anatomical_plane, voxel_size=self.resample,  **merge(self._show_args, kwargs))

    def __repr__(self): return f'{self.__class__.__name__} mode={self.mode} size={"x".join([str(d) for d in self.size])}'

# %% ../nbs/01_vision_core.ipynb 12
class MedImage(MedBase):
    '''Subclass of MedBase that represents an image object.'''
    pass

# %% ../nbs/01_vision_core.ipynb 13
class MedMask(MedBase):
    '''Subclass of MedBase that represents an mask object.'''
    _show_args = {'alpha':0.5, 'cmap':'tab20'}
