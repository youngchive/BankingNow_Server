# BankingNow_Server
뱅킹나우 Django Server 입니다.

## 실행방법
1. clone받고 폴더 열기
2. 터미널에서 $ cd BankingServer
3. $ python3 manage.py migrate(안되고 뭐라뭐라하면 $python3 manage.py makemigrations한 다음 다시 migrate)
4. 슈퍼유저를 만들기 위해 $ python3 manage.py createsuperuser 입력해서 유저 만들기(비번 짧다고 뭐라하면 y눌러서 건너뛰기)
5. 실행하려면 $ python3 manage.py runserver인데 통신하려면 맥북 터미널에서 ifconfig해서 ip주소 찾아서 $ python3 manage.py runserver ~.~.~.~\:8000
