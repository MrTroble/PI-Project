git fetch
git stage .
RAND=`date +%S%N`
git commit -m "Autogenerated commit: $RAND" > ../git_log
while read line; do
echo $line
   if ["$line" = "On branch master"] 
   then
     echo "Everthing up to date; Skipping GIT"
   else
     echo ""
   fi
done < ../git_log
rm -f ../git_log
git pull
git push
python3 test.py
read -p "Press Enter" ip