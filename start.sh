if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/MOH-NIHAAL/delete.git /delete
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /delete
fi
cd /delete
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
