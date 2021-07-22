#conda create -n pyocr python=3.7 && \
#conda init bash && \
#conda init zsh && \
conda activate pyocr && \
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r ./requirements.txt && \
python main.py