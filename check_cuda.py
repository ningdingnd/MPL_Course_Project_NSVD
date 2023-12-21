import torch

# 检查是否支持 CUDA
print(torch.cuda.is_available())

print(torch.__version__)


# 打印当前 CUDA 设备数量
print(torch.cuda.device_count())

# 打印当前使用的 CUDA 设备索引
print(torch.cuda.current_device())

# 打印当前使用的 CUDA 设备名称
print(torch.cuda.get_device_name(torch.cuda.current_device()))

print(torch.version.cuda)
print(torch.backends.cudnn.enabled)
print(torch.__config__.show())


'''未安装 CUDA Toolkit：

PyTorch 需要 CUDA Toolkit 来支持 GPU 加速。确保你已经正确安装了与你的 PyTorch 版本兼容的 CUDA Toolkit。你可以在 PyTorch 的官方网站或 CUDA Toolkit 的官方网站上找到相应版本的信息。
PyTorch 版本不匹配：

请确保你安装的 PyTorch 版本与你的 CUDA Toolkit 版本兼容。查看 PyTorch 文档以获取关于 PyTorch 和 CUDA 版本兼容性的信息。
使用 CPU 版本的 PyTorch：

如果你使用的是 PyTorch 的 CPU 版本而不是 GPU 版本，就会出现这个错误。确保你安装了 PyTorch GPU 版本，例如通过以下命令安装：
bash
Copy code
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
环境变量设置问题：

在有多个 CUDA 版本的系统上，可能会发生环境变量混淆的情况。确保你的系统环境变量中设置了正确的 CUDA 相关路径。
重新安装 PyTorch：

有时，重新安装 PyTorch 可能会解决问题。首先使用 pip 卸载当前的 PyTorch 版本，然后重新安装。确保在安装时提供正确的 CUDA 版本。
bash
Copy code
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu113/torch_stable.html
操作系统兼容性：

某些版本的 PyTorch 和 CUDA 可能与特定操作系统不兼容。检查 PyTorch 和 CUDA 的文档，确保它们支持你正在使用的操作系统。
请注意，具体的解决方法取决于你的操作系统、CUDA 版本和 PyTorch 版本。确保你的系统环境和库版本都是兼容的。如果问题仍然存在，请参阅 PyTorch 和 CUDA 的官方文档，或在相关社区寻求帮助。'''