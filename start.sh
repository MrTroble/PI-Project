git fetch
git stage .
RAND=`date +%S%N`
git commit -m "Autogenerated commit: $RAND" > ../git_log
while read line; do
echo $line
   case $line in "Your branch is up-to-date"*)
     echo "Everthing up to date; Skipping GIT"
   esac
done < ../git_log
rm -f ../git_log
git pull
git push
python3 test.py
read -p "Press Enter" ip