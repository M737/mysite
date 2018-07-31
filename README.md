# mysite 

我的博客网站，不断完善中

目前有以下app：

**blogs** #博客模块

​	分为 Blogs 和BlogType 两个model，

​	Blogs包含 标题，内容，作者，发布时间以及修改时间， 采用 django-ckeditor为富文本编辑器。

​	BlogType 为博客分类

**word**  # 单词模块

​	分为单词集 和 收藏集 两个板块。

 	单词集：内置一部分单词集，支持用户自创单词集，并上传自己收集的单词。 目前单词集有五大功能：

分别是：卡片记忆， 根据释义写单词，根据单词选释义，新增单词，删除单词。

​	收藏集：需用户登录，支持创建多个收藏集并可设置默认收藏集，将在单词集中看到的单词添加到收藏集

​	ps：各单词均支持单词英式和美式发音。

**user**  # 个人信息模块 

​	在原django-User基础上 增加 昵称，头像，个人简介，以及心情记录功能

​	支持修改头像，修改昵称，绑定邮箱，修改个人简介

**comment** # 评论模块

​	这个是一个 ContentType 模块，可作为博客评论， 单词标记，留言板等。 支持评论自身

**like**  # 点赞模块

​	这也是 ContentType 模块，可对博客，评论，留言等点赞，支持取消点赞

**doudou** # 小工具模块

​	小工具，目前上线的是一个 UI栅格参数的计算公式