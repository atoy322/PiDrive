# https://github.com/doe300/VC4CL/wiki/How-to-get

cd /tmp
wget https://raw.githubusercontent.com/doe300/VC4CL/master/.circleci/get_url.py
wget https://raw.githubusercontent.com/doe300/VC4CL/master/.circleci/build_num.py
curl "https://circleci.com/api/v1.1/project/github/doe300/VC4C?limit=100&filter=successful" --output /tmp/json
curl "https://circleci.com/api/v1.1/project/github/doe300/VC4C/$(python ./build_num.py /tmp/json)/artifacts" --output /tmp/dump
wget -O /tmp/vc4cl-stdlib.deb $(python get_url.py "vc4cl-stdlib-" "/tmp/dump")
wget -O /tmp/vc4c.deb $(python get_url.py "vc4c-" "/tmp/dump")
curl "https://circleci.com/api/v1.1/project/github/doe300/VC4CL?limit=100&filter=successful" --output /tmp/json
curl "https://circleci.com/api/v1.1/project/github/doe300/VC4CL/$(python ./build_num.py /tmp/json)/artifacts" --output /tmp/dump
wget -O /tmp/vc4cl.deb $(python get_url.py "vc4cl-" "/tmp/dump")

sudo dpkg -i /tmp/vc4cl-stdlib.deb
sudo dpkg -i /tmp/vc4c.deb
sudo dpkg -i /tmp/vc4cl.deb
