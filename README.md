本网页不提供注册功能，目前仅支持管理员主动添加信息

下面是运行该网站的所需要的操作

1. 由于没有上传数据库，所以需要进行数据迁移

   ```
   $ python manage.py migrate
   ```

2. 创建管理员用户

   ```
   $ python manage.py createsuperuser
   ```

3. 运行Web应用

   ```
   $ python manage.py runserver
   ```

4. 进入`localhost:8000/admin`手动添加User信息；

   或者直接从Django ORM操作数据库批量插入数据

5. 进入`localhost:8000`使用目前的User信息登陆

