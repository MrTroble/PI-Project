git fetch
git stage .
RAND=`date +%S:%N`
echo $RAND
echo $RAND
git commit -m "Autogenerated commit: $RAND"
read -p "Press read " ip
git pull
git push
python3 test.py
read -p "Press [Enter] key" ip