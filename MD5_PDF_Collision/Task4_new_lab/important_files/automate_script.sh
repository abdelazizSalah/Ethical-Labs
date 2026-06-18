
python make_payloads.py 
python build_zips.py 
curl -X POST -F "zipfile=@good.zip" http://icst2.informatik.tu-cottbus.de:1625/sign --output signed.tar
mkdir recieved_data
mv signed.tar recieved_data/
mv evil.zip recieved_data/
cd recieved_data
tar -xvf signed.tar
rm main.zip
rm signed.tar
mv evil.zip main.zip
tar -cvf signed.tar main.zip signature.md5
curl -X POST -F "program=@signed.tar" http://icst2.informatik.tu-cottbus.de:1625/execute