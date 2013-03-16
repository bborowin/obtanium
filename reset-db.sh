read -p "Are you sure? This will obliterate the entirety of everything.. " REPLY
if [[ ! $REPLY =~ yes ]]
then
    exit 1
fi
mysql -u root < db-reset.sql
echo 'Database has been reset'