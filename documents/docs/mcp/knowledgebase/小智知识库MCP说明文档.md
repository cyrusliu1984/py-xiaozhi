# 小智知识库 MCP 说明文档

## 1. 基础安装与 Ollama 模型问题解决

该模块包含 WeKnora 本地知识库服务器安装，及 “找不到 Ollama 模型” 的解决方案。

### 1.1 WeKnora 服务器安装

直接通过官方仓库安装，执行以下步骤：



1. 访问 WeKnora GitHub 地址：[h](https://github.com/Tencent/WeKnora)[ttps:](https://github.com/Tencent/WeKnora)[//gi](https://github.com/Tencent/WeKnora)[thub.](https://github.com/Tencent/WeKnora)[com/T](https://github.com/Tencent/WeKnora)[ence](https://github.com/Tencent/WeKnora)[nt/We](https://github.com/Tencent/WeKnora)[Knora](https://github.com/Tencent/WeKnora)

2. 按照仓库内官方指引，完成本地知识库服务器部署。

### 1.2 Ollama 模型找不到的解决方案

若部署后无法识别 Ollama 模型，需配置服务文件并启动服务，具体操作如下：

#### 步骤 1：配置 ollama.service 文件



* 文件路径：`/etc/systemd/system/ollama.service`

* 文件内容：



```
\[Unit]

Description=Ollama Service

After=network-online.target

\[Service]

ExecStart=/usr/local/bin/ollama serve

User=ollama

Group=ollama

Restart=always

RestartSec=3

Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"

\# 添加内容（允许外部访问）

Environment="OLLAMA\_HOST=0.0.0.0"

\[Install]

WantedBy=default.target
```

#### 步骤 2：启动 Ollama 服务

运行以下指令，后台启动服务并定向输出（避免终端阻塞）：



```
OLLAMA\_HOST=0.0.0.0:11434 ollama serve > /dev/null 2>&1 < /dev/null &
```

## 2. 核心环境配置参数

该模块汇总知识库运行所需的关键环境变量与固定 ID，可直接引用或修改。



| 参数名称         | 取值（默认 / 示例）                                                                                                                  | 说明                                            |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| BASE\_URL    | [http://localhost:80](http://localhost:8080/api/v1)[80/ap](http://localhost:8080/api/v1)[i/v1](http://localhost:8080/api/v1) | 知识库 API 基础路径，可通过环境变量 `KNOWLEDGE_BASE_URL` 自定义 |
| API\_KEY     | sk-W1BUWaIuoac11EGT6eO-6mwihz\_q9QK\_Eokrh-fHK-mSeJ6T                                                                        | 知识库访问密钥，可通过环境变量 `KNOWLEDGE_API_KEY` 自定义       |
| kb\_chat\_id | a54ec473-478a-4358-b2fa-0c19337abc60                                                                                         | 对话关联的知识库对话窗口 ID，固定值（无需修改）                     |

## 3. 知识库详细配置（以 “青龙” 知识库为例）

以实际 “青龙全尺寸通用人形机器人” 知识库为例，明确知识库基本信息与模型配置要求。

### 3.1 知识库基本信息



| 配置项    | 内容                                                                            |
| ------ | ----------------------------------------------------------------------------- |
| 知识库名称  | 青龙                                                                            |
| 知识库描述  | “青龙全尺寸通用人形机器人” 知识库，从产品介绍、技术参数、核心部件三大维度，详细披露其硬件开源相关信息，整体呈现机器人的仿生设计、性能指标与关键组件配置 |
| 知识库 ID | 26d56615-d0c1-4869-8a46-4e4805f5ebef（从知识库页面 URL 中获取，如 `xxx?id=xxx` 后的参数）      |

### 3.2 模型配置

包含 LLM 大语言模型、Embedding 嵌入模型、Rerank 重排模型三类配置，均为必填项。

#### 3.2.1 LLM 大语言模型

![参数设置](documents/docs/mcp/knowledgebase/zhishi1.png)

* 模型来源：二选一（Ollama 本地部署 / Remote API 远程调用）

* 模型名称：示例为 `qwen2:0.6b`（需根据实际部署的模型名称填写）

#### 3.2.2 Embedding 嵌入模型



* 模型来源：二选一（Ollama 本地部署 / Remote API 远程调用）

* 模型名称：示例为 `nomic-embed-text:latest`（需手动输入，不可默认选择）

* 维度要求：必须为有效整数，常见取值为 768、1024、1536、3584 等（需与模型实际输出维度一致）

#### 3.2.3 Rerank 重排模型



* 状态：默认启用（建议保持开启，提升知识库检索准确性）

## 4. 文件上传操作

通过 WeKnora 页面上传知识库关联文件，支持补充硬件开源等核心内容。

### 4.1 上传入口
![上传入口](documents/docs/mcp/knowledgebase/zhishi2.png)

在 WeKnora 知识库管理页面（以 “青龙” 知识库为例，进入对应知识库详情页），找到 **“上传知识”** 功能入口（通常为按钮或图标形式），点击后触发文件选择窗口，即可选择本地文件上传。

> 提示：支持上传的文件格式通常包括 PDF、DOCX、TXT 等，具体以 WeKnora 页面提示为准；建议上传前整理好 “青龙机器人” 的硬件参数表、开源文档等核心内容，确保知识库信息完整。

> （注：文档部分内容可能由 AI 生成）