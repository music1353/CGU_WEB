FROM node:11.2.0

# 安裝nginx跟yarn
RUN apt-get update \
    # && npm install npm@latest -g \
    && apt-get install -y nginx \
    && apt-get install -y yarn

# 指定工作目錄
WORKDIR /app

# 將當前所有文件複製到app資料下
COPY . /app/

# 運行時容器的port
EXPOSE 80

# 1. 安裝dependencies
# 2. run build
# 3. 將dist的文件都複製到nginx的目錄下
# 4. 刪除工作目錄的文件，尤其是node_modules縮小鏡像體積
RUN rm -rf node_modules \
    && yarn install --no-bin-links \
    && yarn run build \
    && cp -r dist/* /var/www/html \
    && cp -r nginx_conf/* /etc/nginx \
    && rm -rf /app

# 以前台方式啟動 nginx
CMD ["nginx", "-g", "daemon off;"]
