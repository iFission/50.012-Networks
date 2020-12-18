python3 demo_receiver.py ss
python3 demo_sender.py ss

python3 demo_receiver.py gbn
python3 demo_sender.py gbn

python3 file_receiver.py gbn file_test_rcv.txt
python3 file_sender.py gbn file_test.txt

python3 demo_receiver.py sr
python3 demo_sender.py sr

python3 file_receiver.py sr file_test_rcv.txt
python3 file_sender.py sr file_test.txt
md5 file_test.txt file_test_rcv.txt

python3 file_receiver.py sr ss_rcv.png
python3 file_sender.py sr ss.png
md5 ss.png ss_rcv.png
