Пример API Сервиса для магазина

[Документация по запросам в PostMan](https://documenter.getpostman.com/view/5037826/SVfJUrSc) - export запросов Postman в ./Data

## **Использование**
    python.exe .\manage.py spectacular --color --file schema.yaml

## **Получить исходный код**

    git config --global user.name "YOUR_USERNAME"
    
    git config --global user.email "your_email_address@example.com"
    
    mkdir ~/my_diplom
    
    cd my_diplom
    
    git clone git@github.com:Dimelsondroid/Diplom_final.git
    
    cd Diplom_final
    
    sudo pip3 install --upgrade pip
    
    sudo pip3 install -r requirements.txt
    
    python3 manage.py makemigrations
     
    python3 manage.py migrate
    
    python3 manage.py createsuperuser    
    
 
**Проверяем работу модулей**
    
    
    python3 manage.py runserver 0.0.0.0:8000
    
   
