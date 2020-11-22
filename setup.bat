conda create -y --name mltest python=3.7 & conda activate mltest & conda install -y -c anaconda -c conda-forge -c pytorch numpy opencv h5py tensorflow tk pillow torchvision cudatoolkit imutils scikit-learn git cython gitlfs & pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI" & pip install "git+https://github.com/DGMaxime/detectron2-windows.git" & git lfs pull