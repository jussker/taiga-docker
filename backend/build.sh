 #!/usr/bin/env bash

image_name=$1

if [[ -d taiga-back ]]; then
    rm -rf taiga-back
fi

git clone -b stable --single-branch https://github.com/taigaio/taiga-back.git
#git clone https://github.com/taigaio/taiga-back.git

if [[ $OSTYPE != darwin* ]]; then
    sed -i 's/^enum34/#enum34/' taiga-back/requirements.txt
    sed -i -e '/sample_data/s/^/#/' taiga-back/regenerate.sh
else
    sed -i '.bak' 's/^enum34/#enum34/' taiga-back/requirements.txt
    sed -i '.bak' '/sample_data/s/^/#/' taiga-back/regenerate.sh
fi

cp taiga-back/requirements.txt .

docker build -t ${image_name} .

if [[ -d taiga-back ]]; then
    rm -rf taiga-back
fi
