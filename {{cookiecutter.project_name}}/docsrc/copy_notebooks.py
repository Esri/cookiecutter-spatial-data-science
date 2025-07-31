from pathlib import Path
import shutil

notebook_src = Path(__file__).parent.parent / 'notebooks'
notebook_dst = Path(__file__).parent / 'notebooks'

shutil.copytree(notebook_src, notebook_dst)
