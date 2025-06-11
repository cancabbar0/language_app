# Language Learning Application With Django
Django ile çoklu dil desteği ile kelime öğreten bir uygulama geliştirdim. Uygulama; kullanıcının login, register gibi işlemleri yapan "accounts" ve kelime öğrenme kısımlarını kontrol eden "language_app" olmak üzere 2 kısımdan oluşuyor. Detayları görmek için bu kısımları inceleyebilirsiniz.

![Screenshot from 2025-02-27 14-47-24](https://github.com/user-attachments/assets/9729c980-2832-4f55-8638-8faadbbe4466)

![image](https://github.com/user-attachments/assets/6f54c33a-76e5-4b14-a05a-a435353f0198)

![image](https://github.com/user-attachments/assets/537eef7f-4fa8-4dec-986f-4b095ac95942)

![image](https://github.com/user-attachments/assets/cc000749-b8ef-417f-b448-cb7c09b32c33)


![image](https://github.com/user-attachments/assets/ef6b5b12-802e-4b24-85d4-41248e54bf1a)



## Uygulamayı Çalıştırmak İçin Şunları Yapmanız Yeterli: 

### virtual env i kur:
	# Linux:
	python3.12 -m venv .venv
	source .venv/bin/activate
	
	# Windows:
	python3.12 -m venv .venv
	.venv\Scripts\activate


### Gerekli dosyaları indir
	pip install -r requirements.txt

### Migration'ları Çalıştır:
	python manage.py makemigrations
 	python manage.py migrate

### Server'ı Çalıştır:.
	python manage.py runserver
