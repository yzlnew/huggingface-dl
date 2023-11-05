### 通过 Cloudflare 代理下载 Hugging Face 模型/数据集

以 `liwu/MNBVC` 数据集为例：

1. 参考 [博客](https://xieincz.github.io/post/huggingface-go-jia-su-xia-zai-huggingface-de-mo-xing-he-shu-ju-ji/) 搭建或者使用原博主代理。
2. clone 目标仓库到当前文件夹，为了获取目录结构，需要把 LFS 关掉。

   ```bash
   GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/liwu/MNBVC
   ```

3. 使用以下命令下载：

    ```bash
    python huggingface-dl.py MNBVC \
    --proxy <your_proxy> \
    --repo liwu/MNBVC \
    --patterns *.jsonl *.jsonl.gz
    ```

### 感谢

- [huggingface-go](https://github.com/xieincz/huggingface-go)