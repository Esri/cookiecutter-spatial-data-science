from pathlib import Path
import os
import re

dir_prj = dir_prj = Path(__file__).parent.parent.parent

def create_slides(notebook_source:Path=None):
    
    sld_dir = dir_prj/'reports'/'presentations'
    
    notebook_source = dir_prj/'notebooks' if notebook_source is None else notebook_source
    
    if notebook_source.is_file():
        assert notebook_source.sufix == '.ipynb', 'Notebook source, if using a file, must be a Juptyer Notebook instance with a ".ipynb" extension.'
        nb_pth_lst = [notebook_source]
        
    else:
        regex = re.compile(r'\d{2,6}-.*\.ipynb')
        nb_pth_lst = [pth for pth in notebook_source.glob('*.ipynb') if regex.match(pth.name)]

    if not sld_dir.exists():
        sld_dir.mkdir(parents=True)

    out_lst = []
    
    for nb_pth in nb_pth_lst:
        os.system(f'jupyter nbconvert "{nb_pth}" --to slides --output-dir="{sld_dir}"')
        out_lst.append(sld_dir/f'{nb_pth.name}.slides.html')
        
    return out_lst

if __name__ == "__main__":

    create_slides()