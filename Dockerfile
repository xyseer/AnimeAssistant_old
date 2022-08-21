FROM python:3.9
WORKDIR /app
COPY ./*.py /app/
COPY ./requirements.txt /app/requirements.txt
COPY ./static /app/static
EXPOSE 12138
#RUN sed -i 's@dl-cdn.alpinelinux.org@mirrors.aliyun.com@g' /etc/apk/repositories
#RUN sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
#RUN sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
RUN sed -i 's|security.debian.org|mirrors.ustc.edu.cn|g' /etc/apt/sources.list
RUN sed -i 's|deb.debian.org|mirrors.ustc.edu.cn|g' /etc/apt/sources.list
#RUN apt update
#RUN apt install -y python3 python3-pip
RUN pip3 install -r /app/requirements.txt -i "https://pypi.tuna.tsinghua.edu.cn/simple"
RUN apt update
RUN apt install libgl1-mesa-glx -y
#RUN apk update
#RUN apk add dpkg
#RUN dpkg --add-architecture amd64
#RUN dpkg -i /app/go-cqhttp_1.0.0-rc3_linux_amd64.deb
#RUN apk add ffmpeg
#RUN apk del dpkg
CMD ["python3","main.py"]
#CMD "go-cqhttp"

