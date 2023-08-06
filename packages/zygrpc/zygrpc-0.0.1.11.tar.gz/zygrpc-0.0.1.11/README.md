# libzygrpc

智眼Grpc SDK

## 生成gRPC代码

安装依赖：

`pip install -U grpcio protobuf grpcio-tools`

生成gRPC代码：

在libzygrpc目录下运行

`python -m grpc_tools.protoc -I . --python_out=python/ --grpc_python_out=python/ proto/zhiyan_rpc.proto`

gRPC工具会生成两个Python文件：

* proto/zhiyan_rpc_pb2.py
* proto/zhiyan_rpc_pb2_grpc.py

## 注意事项

生成 `proto/zhiyan_rpc_pb2_grpc.py` 文件后，需要确认其中导入 `zhiyan_rpc_pb2.py` 是否正确：

```python
from proto import zhiyan_rpc_pb2 as proto_dot_zhiyan__rpc__pb2
```

## 安装SDK

### 从 pip 安装

`pip install -U zygrpc`

### 使用方法

#### 使用

比如：

`from proto import zhiyan_rpc_pb2`

### 本地打包安装

#### 打包

安装依赖包：

`pip install -U setuptools wheel`

运行：

`rm -rf build/ dist/ zygrpc.egg-info/ && python setup.py bdist_wheel`

在 `dist` 目录下会生成类似 `zygrpc-1.0.0-py3-none-any.whl` 的安装包。

#### 本地安装

全局安装：

`sudo pip install -U dist/zygrpc-0.0.1-py3-none-any.whl`

用户目录安装：

`pip install --user -U dist/zygrpc-0.0.1-py3-none-any.whl`

#### 卸载

`pip uninstall zygrpc`
