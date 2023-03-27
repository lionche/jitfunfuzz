#下载基础镜像
# FROM nvidia/cuda:11.4.2-cudnn8-runtime-ubuntu20.04
# FROM nvidia/cuda:11.8.0-devel-ubuntu20.04
#FROM ubuntu:20.04
FROM swift:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip git openssh-server curl locales clang vim proxychains&& rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN python -m pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pyyaml pymysql django django-tables2 tzdata DBUtils -i https://pypi.tuna.tsinghua.edu.cn/simple
# # RUN pip install torch accelerate protobuf datasets "chardet<3.1.0" "urllib3<=1.25" "sentencepiece<0.1.92" sklearn transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip install torch accelerate protobuf datasets "chardet<3.1.0" "urllib3==1.25" sentencepiece scikit-learn transformers -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN sed -ie 's/# zh_cn.uTF-8 UTF-8/zh_CN.UTF-8 UTF-8/g' /etc/locale.gen
RUN locale-gen
ENV LANG zh_CN.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME /root

# # 安装node
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - && apt-get install -y nodejs
RUN npm npm install nyc jsvu jshint commander -g --registry=http://registry.npmmirror.com
RUN npm install --save-dev @babel/core -g --registry=http://registry.npmmirror.com
ENV NODE_PATH /usr/lib/node_modules/
ENV FUZZOPT /root/fuzzopt

# #拷贝引擎
# ADD jsvu.tar.gz /root/
# #拷贝数据集
WORKDIR $FUZZOPT

#开启ssh服务
RUN mkdir /var/run/sshd
RUN echo 'root:123123' | chpasswd
RUN echo "Port 18889" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo "service ssh restart" >> ~/.bashrc


# ENV http_proxy socks5://10.15.0.35:20170
# ENV https_proxy socks5://10.15.0.35:20170
# LABEL key="value12"
RUN git clone --depth=1 -b main https://github.com/lionche/fuzzopt.git $FUZZOPT
# RUN git clone --depth=1 https://github.com/lionche/fuzzopt.git $FUZZOPT
RUN tar -zxvf $FUZZOPT/data/JStestcases.tar.gz -C $FUZZOPT/data/
RUN rm -rf $FUZZOPT/data/JStestcases.tar.gz
# ENV http_proxy ""
# ENV https_proxy ""
RUN pip install PyExecJS tqdm -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD engine /root/engine
#RUN wget http://security.ubuntu.com/ubuntu/pool/main/i/icu/libicu66_66.1-2ubuntu2_amd64.deb && dpkg -i libicu66_66.1-2ubuntu2_amd64.deb && rm libicu66_66.1-2ubuntu2_amd64.deb
#RUN wget http://security.ubuntu.com/ubuntu/pool/main/i/icu/libicu60_60.2-3ubuntu3.2_amd64.deb && dpkg -i libicu60_60.2-3ubuntu3.2_amd64.deb && rm libicu60_60.2-3ubuntu3.2_amd64.deb
